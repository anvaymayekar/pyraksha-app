from typing import Callable, Optional
from kivy.utils import platform


class PermissionManager:
    _instance: Optional["PermissionManager"] = None

    def __init__(self):
        self._permission_handlers: dict[str, Callable] = {}

    @classmethod
    def get_instance(cls) -> "PermissionManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def request_location_permission(
        self, callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        if platform == "android":
            from android.permissions import request_permissions, Permission

            permissions = [
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
            ]

            def on_permission_result(permissions_result, grant_results):
                granted = all(grant_results)
                if callback:
                    callback(granted)

            request_permissions(permissions, on_permission_result)
        else:
            if callback:
                callback(True)

    def check_location_permission(self) -> bool:
        if platform == "android":
            from android.permissions import check_permission, Permission

            return check_permission(
                Permission.ACCESS_FINE_LOCATION
            ) and check_permission(Permission.ACCESS_COARSE_LOCATION)
        return True

    def request_sms_permission(
        self, callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        if platform == "android":
            from android.permissions import request_permissions, Permission

            permissions = [Permission.SEND_SMS]

            def on_permission_result(permissions_result, grant_results):
                granted = all(grant_results)
                if callback:
                    callback(granted)

            request_permissions(permissions, on_permission_result)
        else:
            if callback:
                callback(True)

    def check_sms_permission(self) -> bool:
        if platform == "android":
            from android.permissions import check_permission, Permission

            return check_permission(Permission.SEND_SMS)
        return True
