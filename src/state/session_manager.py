from typing import Optional
from datetime import datetime, timedelta
from src.models.user import User
from src.services.storage_service import StorageService
from src.config.app_config import AppConfig


class SessionManager:
    _instance: Optional["SessionManager"] = None

    def __init__(self):
        self._storage = StorageService.get_instance()

    @classmethod
    def get_instance(cls) -> "SessionManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def save_session(self, user: User) -> bool:
        session_data = {"user": user.to_dict(), "timestamp": datetime.now().isoformat()}
        return self._storage.save(AppConfig.SESSION_FILE, session_data)

    def load_session(self) -> Optional[User]:
        session_data = self._storage.load(AppConfig.SESSION_FILE)

        if not session_data:
            return None

        try:
            timestamp = datetime.fromisoformat(session_data["timestamp"])
            age = datetime.now() - timestamp

            if age > timedelta(days=AppConfig.SESSION_TIMEOUT_DAYS):
                self.clear_session()
                return None

            user = User.from_dict(session_data["user"])
            return user
        except Exception as e:
            print(f"Failed to load session: {e}")
            self.clear_session()
            return None

    def clear_session(self) -> bool:
        return self._storage.delete(AppConfig.SESSION_FILE)

    def is_session_valid(self) -> bool:
        return self.load_session() is not None
