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
        data = self._storage.load(AppConfig.ACTIVE_SOS_FILE)
        if data:
            sos = SOS.from_dict(data)
            if sos.status == SOSStatus.ACTIVE:
                self._active_sos = sos

    def _save_active_sos(self) -> bool:
        if self._active_sos:
            return self._storage.save(
                AppConfig.ACTIVE_SOS_FILE, self._active_sos.to_dict()
            )
        else:
            return self._storage.delete(AppConfig.ACTIVE_SOS_FILE)

    def _save_to_history(self, sos: SOS) -> bool:
        history_data = self._storage.load(AppConfig.SOS_HISTORY_FILE) or []
        history_data.append(sos.to_dict())
        return self._storage.save(AppConfig.SOS_HISTORY_FILE, history_data)

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

        response = self._api_client.trigger_sos(new_sos.sos_id, initial_location)

        if not response.get("success"):
            print(f"Backend sync failed: {response.get('message')}")

        self._active_sos = new_sos

        if self._save_active_sos():
            self._location_service.start_tracking()
            return True, "SOS activated", new_sos
        else:
            self._active_sos = None
            return False, "Failed to activate SOS", None

    def resolve_sos(self) -> tuple[bool, str]:
        if not self._active_sos:
            return False, "No active SOS to resolve"

        self._active_sos.resolve()
        self._location_service.stop_tracking()

        response = self._api_client.resolve_sos(self._active_sos.sos_id)

        if not response.get("success"):
            print(f"Backend sync failed: {response.get('message')}")

        if self._save_to_history(self._active_sos):
            resolved_sos = self._active_sos
            self._active_sos = None
            self._storage.delete(AppConfig.ACTIVE_SOS_FILE)
            return True, "SOS resolved successfully"
        else:
            return False, "Failed to save SOS to history"

    def get_active_sos(self) -> Optional[SOS]:
        return self._active_sos

    def update_location(self, location: Location) -> bool:
        if self._active_sos and location:
            self._active_sos.add_location(location)

            location_data = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "accuracy": location.accuracy,
                "timestamp": location.timestamp.isoformat(),
            }

            response = self._api_client.update_sos_location(
                self._active_sos.sos_id, location_data
            )

            if not response.get("success"):
                print(f"Location sync failed: {response.get('message')}")

            return self._save_active_sos()
        return False

    def get_sos_history(self, user_id: str) -> List[SOS]:
        history_data = self._storage.load(AppConfig.SOS_HISTORY_FILE) or []
        all_sos = [SOS.from_dict(data) for data in history_data]
        return [sos for sos in all_sos if sos.user_id == user_id]
