import uuid
from typing import Optional, List
from datetime import datetime
from src.models.sos import SOS
from src.models.location import Location
from src.config.constants import SOSStatus
from src.services.storage_service import StorageService
from src.services.location_service import LocationService
from src.services.api_client import APIClient
from src.config.app_config import AppConfig


class SOSService:
    _instance: Optional["SOSService"] = None

    def __init__(self):
        self._storage = StorageService.get_instance()
        self._location_service = LocationService.get_instance()
        self._api_client = APIClient.get_instance()
        self._active_sos: Optional[SOS] = None
        self._load_active_sos()

    @classmethod
    def get_instance(cls) -> "SOSService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def active_sos(self) -> Optional[SOS]:
        return self._active_sos

    def _load_active_sos(self) -> None:
        try:
            data = self._storage.load(AppConfig.ACTIVE_SOS_FILE)
            if data:
                sos = SOS.from_dict(data)
                if sos.status == SOSStatus.ACTIVE:
                    self._active_sos = sos
        except Exception as e:
            print(f"Error loading active SOS: {e}")

    def _save_active_sos(self) -> bool:
        try:
            if self._active_sos:
                return self._storage.save(
                    AppConfig.ACTIVE_SOS_FILE, self._active_sos.to_dict()
                )
            else:
                return self._storage.delete(AppConfig.ACTIVE_SOS_FILE)
        except Exception as e:
            print(f"Error saving active SOS: {e}")
            return False

    def _save_to_history(self, sos: SOS) -> bool:
        try:
            history_data = self._storage.load(AppConfig.SOS_HISTORY_FILE) or []
            history_data.append(sos.to_dict())
            return self._storage.save(AppConfig.SOS_HISTORY_FILE, history_data)
        except Exception as e:
            print(f"Error saving to history: {e}")
            return False

    def sync_from_backend(self) -> bool:
        try:
            print("Syncing SOS events from backend...")
            response = self._api_client.get_sos_history()

            if not response:
                print("No response from backend")
                return False

            if not response.get("success"):
                print(f"Backend error: {response.get('message')}")
                return False

            backend_sos_data = response.get("sos_events", [])
            print(f"Received {len(backend_sos_data)} SOS events from backend")

            if not backend_sos_data:
                print("ℹNo SOS events from backend")
                return True

            backend_sos_list = []
            for sos_data in backend_sos_data:
                try:
                    status_str = sos_data.get("status", "active")

                    try:
                        status = SOSStatus[status_str.upper()]
                    except (KeyError, AttributeError):
                        print(f"Unknown SOS status '{status_str}', using ACTIVE")
                        status = SOSStatus.ACTIVE

                    sos = SOS(
                        sos_id=sos_data["sos_id"],
                        user_id=str(sos_data["user_id"]),
                        status=status,
                    )

                    if "start_time" in sos_data and sos_data["start_time"]:
                        try:
                            sos.start_time = datetime.fromisoformat(
                                sos_data["start_time"].replace("Z", "+00:00")
                            )
                        except:
                            sos.start_time = datetime.now()

                    if "end_time" in sos_data and sos_data["end_time"]:
                        try:
                            sos.end_time = datetime.fromisoformat(
                                sos_data["end_time"].replace("Z", "+00:00")
                            )
                        except:
                            pass

                    backend_sos_list.append(sos)
                    print(f"Parsed SOS: {sos.sos_id} - Status: {sos.status.value}")

                except KeyError as e:
                    print(f"Missing field in SOS data: {e}")
                    continue
                except Exception as e:
                    print(f"Error parsing SOS: {e}")
                    import traceback

                    traceback.print_exc()
                    continue

            if backend_sos_list:
                history_data = [sos.to_dict() for sos in backend_sos_list]
                saved = self._storage.save(AppConfig.SOS_HISTORY_FILE, history_data)
                if saved:
                    print(f"Saved {len(backend_sos_list)} SOS events locally")
                    return True
                else:
                    print("Failed to save SOS events locally")
                    return False
            else:
                print("No valid SOS events parsed")
                return False

        except Exception as e:
            print(f"SOS sync failed with exception: {e}")
            import traceback

            traceback.print_exc()
            return False

    def trigger_sos(self, user_id: str) -> tuple[bool, str, Optional[SOS]]:
        if self._active_sos:
            return False, "An SOS is already active", self._active_sos

        new_sos = SOS(
            sos_id=str(uuid.uuid4()), user_id=user_id, status=SOSStatus.ACTIVE
        )

        new_sos.activate()

        current_location = self._location_service.get_current_location()
        if current_location:
            new_sos.add_location(current_location)

        initial_location = None
        if current_location:
            initial_location = {
                "latitude": current_location.latitude,
                "longitude": current_location.longitude,
                "accuracy": current_location.accuracy,
                "timestamp": current_location.timestamp.isoformat(),
            }

        try:
            print(f"Triggering SOS to backend: {new_sos.sos_id}")
            response = self._api_client.trigger_sos(new_sos.sos_id, initial_location)

            if response and response.get("success"):
                print("SOS triggered on backend successfully")
            else:
                error_msg = (
                    response.get("message", "Unknown error")
                    if response
                    else "No response"
                )
                print(f"Backend SOS trigger failed: {error_msg}")
        except Exception as e:
            print(f"Error triggering SOS on backend: {e}")

        self._active_sos = new_sos

        if self._save_active_sos():
            self._location_service.start_tracking()
            return True, "SOS activated", new_sos
        else:
            self._active_sos = None
            return False, "Failed to activate SOS", None

    def update_location(self, location: Location) -> bool:
        if self._active_sos and location:
            self._active_sos.add_location(location)

            location_data = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "accuracy": location.accuracy,
                "timestamp": location.timestamp.isoformat(),
            }

            try:
                response = self._api_client.update_sos_location(
                    self._active_sos.sos_id, location_data
                )

                if response and response.get("success"):
                    print(f"Location updated on backend")
                else:
                    print(f"Location update failed on backend")
            except Exception as e:
                print(f"Error updating location on backend: {e}")

            return self._save_active_sos()
        return False

    def resolve_sos(self) -> tuple[bool, str]:
        if not self._active_sos:
            return False, "No active SOS to resolve"

        self._active_sos.resolve()
        self._location_service.stop_tracking()

        try:
            print(f"Resolving SOS on backend: {self._active_sos.sos_id}")
            response = self._api_client.resolve_sos(self._active_sos.sos_id)

            if response and response.get("success"):
                print("SOS resolved on backend successfully")
            else:
                error_msg = (
                    response.get("message", "Unknown error")
                    if response
                    else "No response"
                )
                print(f"Backend SOS resolve failed: {error_msg}")
        except Exception as e:
            print(f"Error resolving SOS on backend: {e}")

        if self._save_to_history(self._active_sos):
            resolved_sos = self._active_sos
            self._active_sos = None
            self._storage.delete(AppConfig.ACTIVE_SOS_FILE)
            return True, "SOS resolved successfully"
        else:
            return False, "Failed to save SOS to history"

    def get_user_sos_history(self, user_id: str) -> List[SOS]:
        print(f"Getting SOS history for user: {user_id}")

        synced = self.sync_from_backend()
        if synced:
            print("Sync successful, loading from local storage")
        else:
            print("Sync failed, using cached data")

        try:
            history_data = self._storage.load(AppConfig.SOS_HISTORY_FILE) or []
            all_sos = [SOS.from_dict(data) for data in history_data]
            user_sos = [sos for sos in all_sos if sos.user_id == user_id]

            sorted_sos = sorted(user_sos, key=lambda x: x.start_time, reverse=True)
            print(f"Found {len(sorted_sos)} SOS events for user")

            for sos in sorted_sos:
                print(f"  - {sos.sos_id}: {sos.status.value}")

            return sorted_sos
        except Exception as e:
            print(f"Error loading SOS history: {e}")
            return []

    def get_active_sos_by_user(self, user_id: str) -> Optional[SOS]:
        if self._active_sos and self._active_sos.user_id == user_id:
            return self._active_sos
        return None
