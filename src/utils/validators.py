import re
from typing import Tuple


class Validators:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        if not email:
            return False, "Email is required"

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            return False, "Invalid email format"

        return True, ""

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        if not phone:
            return False, "Phone number is required"

        phone_clean = re.sub(r"[^0-9]", "", phone)
        if len(phone_clean) < 10:
            return False, "Phone number must be at least 10 digits"

        return True, ""

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        if not password:
            return False, "Password is required"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        return True, ""

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if not name:
            return False, "Name is required"

        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"

        return True, ""

    @staticmethod
    def validate_non_empty(value: str, field_name: str) -> Tuple[bool, str]:
        if not value or not value.strip():
            return False, f"{field_name} is required"
        return True, ""
