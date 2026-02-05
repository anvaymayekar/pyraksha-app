from typing import Optional, Callable
from kivy.utils import platform
from src.models.location import Location
from src.core.permissions import PermissionManager


class LocationService:
    _instance: Optional["LocationService"] = None

    def __init__(self):
        self._current_location: Optional[Location] = None
        self._is_tracking = False
        self._permission_manager = PermissionManager.get_instance()
        self._gps = None

        if platform == "android":
            from plyer import gps

            self._gps = gps

    @classmethod
    def get_instance(cls) -> "LocationService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def current_location(self) -> Optional[Location]:
        return self._current_location

    @property
    def is_tracking(self) -> bool:
        return self._is_tracking

    def _on_location_update(self, **kwargs) -> None:
        latitude = kwargs.get("lat")
        longitude = kwargs.get("lon")
        accuracy = kwargs.get("accuracy")

        if latitude is not None and longitude is not None:
            self._current_location = Location(
                latitude=latitude, longitude=longitude, accuracy=accuracy
            )

    def _on_status(self, stype, status) -> None:
        if stype == "provider-enabled":
            print("GPS provider enabled")
        elif stype == "provider-disabled":
            print("GPS provider disabled")

    def request_permissions(
        self, callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        self._permission_manager.request_location_permission(callback)

    def start_tracking(self) -> bool:
        if not self._permission_manager.check_location_permission():
            return False

        if self._gps and not self._is_tracking:
            try:
                self._gps.configure(
                    on_location=self._on_location_update, on_status=self._on_status
                )
                self._gps.start(minTime=1000, minDistance=0)
                self._is_tracking = True
                return True
            except Exception as e:
                print(f"Failed to start GPS tracking: {e}")
                return False

        return False

    def stop_tracking(self) -> None:
        if self._gps and self._is_tracking:
            try:
                self._gps.stop()
                self._is_tracking = False
            except Exception as e:
                print(f"Failed to stop GPS tracking: {e}")

    def get_current_location(self) -> Optional[Location]:
        return self._current_location
