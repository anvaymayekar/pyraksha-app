import hashlib
import uuid
from typing import Optional, List
from src.models.user import User
from src.services.storage_service import StorageService
from src.services.api_client import APIClient
from src.config.app_config import AppConfig


class AuthService:
    _instance: Optional["AuthService"] = None

    def __init__(self):
        self._storage = StorageService.get_instance()
        self._api_client = APIClient.get_instance()

    @classmethod
    def get_instance(cls) -> "AuthService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> List[User]:
        data = self._storage.load(AppConfig.USERS_FILE)
        if not data:
            return []
        return [User.from_dict(user_data) for user_data in data]

    def _save_users(self, users: List[User]) -> bool:
        data = [user.to_dict() for user in users]
        return self._storage.save(AppConfig.USERS_FILE, data)

    def _find_user_by_email(self, email: str) -> Optional[User]:
        users = self._load_users()
        for user in users:
            if user.email.lower() == email.lower():
                return user
        return None

    def register(
        self, name: str, email: str, phone: str, password: str
    ) -> tuple[bool, str, Optional[User]]:
        if not name or not email or not phone or not password:
            return False, "All fields are required", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters", None

        response = self._api_client.register(name, email, phone, password)

        if response.get("success"):
            user_data = response.get("user")
            if user_data:
                user = User.from_dict(user_data)
                user.password_hash = self._hash_password(password)

                users = self._load_users()
                users.append(user)
                self._save_users(users)

                return True, "Registration successful", user

        existing_user = self._find_user_by_email(email)
        if existing_user:
            return False, "Email already registered", None

        users = self._load_users()

        new_user = User(
            user_id=str(uuid.uuid4()),
            name=name,
            email=email,
            phone=phone,
            password_hash=self._hash_password(password),
        )

        users.append(new_user)

        if self._save_users(users):
            return True, "Registration successful (offline)", new_user
        else:
            return False, "Failed to save user data", None

    def login(self, email: str, password: str) -> tuple[bool, str, Optional[User]]:
        if not email or not password:
            return False, "Email and password are required", None

        response = self._api_client.login(email, password)

        if response.get("success"):
            user_data = response.get("user")
            if user_data:
                user = User.from_dict(user_data)

                users = self._load_users()
                existing_user = next(
                    (u for u in users if u.email.lower() == email.lower()), None
                )

                if existing_user:
                    existing_user.name = user.name
                    existing_user.phone = user.phone
                else:
                    users.append(user)

                self._save_users(users)
                return True, "Login successful", user

        user = self._find_user_by_email(email)
        if not user:
            return False, "Invalid email or password", None

        password_hash = self._hash_password(password)
        if user.password_hash != password_hash:
            return False, "Invalid email or password", None

        return True, "Login successful (offline)", user

    def is_authenticated(self) -> bool:
        from src.state.app_state import AppState

        state = AppState.get_instance()
        return state.is_authenticated
