import uuid
from typing import Optional, List
from src.models.complaint import Complaint
from src.services.storage_service import StorageService
from src.services.api_client import APIClient
from src.config.app_config import AppConfig


class ComplaintService:
    _instance: Optional["ComplaintService"] = None

    def __init__(self):
        self._storage = StorageService.get_instance()
        self._api_client = APIClient.get_instance()

    @classmethod
    def get_instance(cls) -> "ComplaintService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_complaints(self) -> List[Complaint]:
        data = self._storage.load(AppConfig.COMPLAINTS_FILE)
        if not data:
            return []
        return [Complaint.from_dict(complaint_data) for complaint_data in data]

    def _save_complaints(self, complaints: List[Complaint]) -> bool:
        data = [complaint.to_dict() for complaint in complaints]
        return self._storage.save(AppConfig.COMPLAINTS_FILE, data)

    def file_complaint(
        self, user_id: str, title: str, description: str
    ) -> tuple[bool, str, Optional[Complaint]]:
        if not title or not description:
            return False, "Title and description are required", None

        if len(title) < 5:
            return False, "Title must be at least 5 characters", None

        if len(description) < 10:
            return False, "Description must be at least 10 characters", None

        complaints = self._load_complaints()

        new_complaint = Complaint(
            complaint_id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            description=description,
        )

        response = self._api_client.file_complaint(
            new_complaint.complaint_id, title, description
        )

        if not response.get("success"):
            print(f"Backend sync failed: {response.get('message')}")

        complaints.append(new_complaint)

        if self._save_complaints(complaints):
            return True, "Complaint filed successfully", new_complaint
        else:
            return False, "Failed to save complaint", None

    def get_user_complaints(self, user_id: str) -> List[Complaint]:
        all_complaints = self._load_complaints()
        return [c for c in all_complaints if c.user_id == user_id]

    def get_complaint_by_id(self, complaint_id: str) -> Optional[Complaint]:
        complaints = self._load_complaints()
        for complaint in complaints:
            if complaint.complaint_id == complaint_id:
                return complaint
        return None

    def get_all_complaints(self) -> List[Complaint]:
        return self._load_complaints()
