from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class User:
    id: Optional[int] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: Optional[bool] = True

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        data = data.copy()

        # Parse datetime fields safely
        for field_name in ("created_at", "last_login"):
            if field_name in data and isinstance(data[field_name], str):
                try:
                    data[field_name] = datetime.fromisoformat(data[field_name])
                except ValueError:
                    data[field_name] = None

        # Ignore unknown fields like password_hash if present
        allowed_fields = {
            "id",
            "user_id",
            "name",
            "email",
            "phone",
            "role",
            "created_at",
            "last_login",
            "is_active",
        }

        clean_data = {k: v for k, v in data.items() if k in allowed_fields}
        return cls(**clean_data)

    def get_display_name(self) -> str:
        return self.name or ""

    def get_masked_phone(self) -> str:
        if self.phone and len(self.phone) >= 4:
            return f"***{self.phone[-4:]}"
        return self.phone or ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
        }
