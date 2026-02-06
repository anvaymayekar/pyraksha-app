import json
from typing import Optional, Dict, Any
from urllib import request as urllib_request, error
from src.utils.logger import Logger
from src.config.app_config import AppConfig


class APIClient:
    _instance: Optional["APIClient"] = None

    def __init__(self, base_url: str = AppConfig.API_BASE_URL):
        self.base_url = base_url
        self._token: Optional[str] = None

    @classmethod
    def get_instance(cls, base_url: str = AppConfig.API_BASE_URL) -> "APIClient":
        if cls._instance is None:
            cls._instance = cls(base_url)
        return cls._instance

    def set_token(self, token: str) -> None:
        self._token = token

    def clear_token(self) -> None:
        self._token = None

    def _make_request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
        }

        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            if data:
                data_bytes = json.dumps(data).encode("utf-8")
                req = urllib_request.Request(
                    url, data=data_bytes, headers=headers, method=method
                )
            else:
                req = urllib_request.Request(url, headers=headers, method=method)

            with urllib_request.urlopen(req, timeout=10) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                return response_data

        except error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            Logger.log_error(
                "APIClient",
                f"HTTP Error {e.code}: {error_body}",
                e,
            )
            try:
                error_json = json.loads(error_body)
                return error_json
            except:
                return {"success": False, "message": f"HTTP Error {e.code}"}

        except Exception as e:
            Logger.log_error("APIClient", "Request failed", e)
            return {"success": False, "message": str(e)}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        response = self._make_request(
            "/api/auth/login", "POST", {"email": email, "password": password}
        )

        if response.get("success") and response.get("token"):
            self.set_token(response["token"])

        return response

    def register(
        self, name: str, email: str, phone: str, password: str
    ) -> Dict[str, Any]:
        response = self._make_request(
            "/api/auth/register",
            "POST",
            {"name": name, "email": email, "phone": phone, "password": password},
        )

        if response.get("success") and response.get("token"):
            self.set_token(response["token"])

        return response

    def verify_token(self) -> Dict[str, Any]:
        return self._make_request("/api/auth/verify", "POST")

    def trigger_sos(
        self, sos_id: str, initial_location: Optional[Dict] = None
    ) -> Dict[str, Any]:
        data = {"sos_id": sos_id}
        if initial_location:
            data["location"] = initial_location

        return self._make_request("/api/sos/trigger", "POST", data)

    def update_sos_location(self, sos_id: str, location: Dict) -> Dict[str, Any]:
        return self._make_request(
            "/api/sos/update_location", "POST", {"sos_id": sos_id, "location": location}
        )

    def resolve_sos(self, sos_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        data = {"sos_id": sos_id}
        if notes:
            data["notes"] = notes

        return self._make_request("/api/sos/resolve", "POST", data)

    def get_active_sos(self) -> Dict[str, Any]:
        return self._make_request("/api/sos/active", "GET")

    def get_sos_history(self) -> Dict[str, Any]:
        return self._make_request("/api/sos/history", "GET")

    def file_complaint(
        self,
        complaint_id: str,
        title: str,
        description: str,
        user_id: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload = {
            "complaint_id": complaint_id,
            "title": title,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
        }
        if user_id:
            payload["user_id"] = user_id  # send user_id to backend

        return self._make_request("/api/complaints/file", "POST", payload)

    def get_complaints(self, status: Optional[str] = None) -> Dict[str, Any]:
        endpoint = "/api/complaints/list"
        if status:
            endpoint += f"?status={status}"
        return self._make_request(endpoint, "GET")

    def get_complaint(self, complaint_id: str) -> Dict[str, Any]:
        return self._make_request(f"/api/complaints/{complaint_id}", "GET")
