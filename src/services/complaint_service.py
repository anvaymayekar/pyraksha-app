import uuid
from typing import Optional, List
from src.models.complaint import Complaint
from src.services.storage_service import StorageService
from src.services.api_client import APIClient
from src.config.app_config import AppConfig
from src.config.constants import ComplaintStatus
from datetime import datetime


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
        try:
            data = self._storage.load(AppConfig.COMPLAINTS_FILE)
            if not data:
                return []

            complaints = []
            for complaint_data in data:
                try:
                    complaint = Complaint.from_dict(complaint_data)
                    complaints.append(complaint)
                except Exception as e:
                    print(f"Error loading complaint: {e}")
                    continue

            return complaints
        except Exception as e:
            print(f"Error loading complaints file: {e}")
            return []

    def _save_complaints(self, complaints: List[Complaint]) -> bool:
        try:
            data = [complaint.to_dict() for complaint in complaints]
            return self._storage.save(AppConfig.COMPLAINTS_FILE, data)
        except Exception as e:
            print(f"Error saving complaints: {e}")
            return False

    def sync_from_backend(self) -> bool:
        try:
            print("Syncing complaints from backend...")
            response = self._api_client.get_complaints()

            if not response:
                print("No response from backend")
                return False

            if not response.get("success"):
                print(f"Backend error: {response.get('message')}")
                return False

            backend_complaints_data = response.get("complaints", [])
            print(f"Received {len(backend_complaints_data)} complaints from backend")

            if not backend_complaints_data:
                print("No complaints from backend")
                return True

            backend_complaints = []
            for complaint_data in backend_complaints_data:
                try:
                    status_str = complaint_data.get("status", "pending")

                    if isinstance(status_str, str):
                        try:
                            status = ComplaintStatus(status_str)
                        except ValueError:
                            print(f"Unknown status '{status_str}', using PENDING")
                            status = ComplaintStatus.PENDING
                    else:
                        status = ComplaintStatus.PENDING

                    timestamp_str = complaint_data.get("timestamp")
                    if timestamp_str:
                        try:
                            timestamp = datetime.fromisoformat(
                                timestamp_str.replace("Z", "+00:00")
                            )
                        except:
                            timestamp = datetime.now()
                    else:
                        timestamp = datetime.now()

                    complaint = Complaint(
                        complaint_id=complaint_data["complaint_id"],
                        user_id=str(complaint_data["user_id"]),
                        title=complaint_data["title"],
                        description=complaint_data["description"],
                        status=status,
                        timestamp=timestamp,
                    )

                    if (
                        "resolution_notes" in complaint_data
                        and complaint_data["resolution_notes"]
                    ):
                        complaint.resolution_notes = complaint_data["resolution_notes"]

                    backend_complaints.append(complaint)
                    print(
                        f"Parsed: {complaint.title} - Status: {complaint.status.value}"
                    )

                except KeyError as e:
                    print(f"Missing field in complaint data: {e}")
                    continue
                except Exception as e:
                    print(f"Error parsing complaint: {e}")
                    import traceback

                    traceback.print_exc()
                    continue

            if backend_complaints:
                saved = self._save_complaints(backend_complaints)
                if saved:
                    print(f"Saved {len(backend_complaints)} complaints locally")
                    return True
                else:
                    print("Failed to save complaints locally")
                    return False
            else:
                print("No valid complaints parsed")
                return False

        except Exception as e:
            print(f"Sync failed with exception: {e}")
            import traceback

            traceback.print_exc()
            return False

    def file_complaint(
        self, user_id: str, title: str, description: str
    ) -> tuple[bool, str, Optional[Complaint]]:
        if not title or not description:
            return False, "Title and description are required", None

        if len(title) < 5:
            return False, "Title must be at least 5 characters", None

        if len(description) < 10:
            return False, "Description must be at least 10 characters", None

        new_complaint = Complaint(
            complaint_id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            description=description,
        )

        try:
            print(f"Filing complaint to backend: {title}")
            response = self._api_client.file_complaint(
                new_complaint.complaint_id, title, description
            )

            if response and response.get("success"):
                print("Complaint filed to backend successfully")
                complaints = self._load_complaints()
                complaints.append(new_complaint)
                self._save_complaints(complaints)
                return True, "Complaint filed successfully", new_complaint
            else:
                error_msg = (
                    response.get("message", "Unknown error")
                    if response
                    else "No response"
                )
                print(f"Backend filing failed: {error_msg}, saving locally")
                complaints = self._load_complaints()
                complaints.append(new_complaint)
                self._save_complaints(complaints)
                return True, f"Saved locally (will sync later)", new_complaint

        except Exception as e:
            print(f"Error filing complaint: {e}")
            complaints = self._load_complaints()
            complaints.append(new_complaint)
            self._save_complaints(complaints)
            return True, "Saved locally (offline mode)", new_complaint

    def get_user_complaints(self, user_id: str) -> List[Complaint]:
        print(f"Getting complaints for user: {user_id}")

        synced = self.sync_from_backend()
        if synced:
            print("Sync successful, loading from local storage")
        else:
            print("Sync failed, using cached data")

        all_complaints = self._load_complaints()
        user_complaints = [c for c in all_complaints if c.user_id == user_id]

        sorted_complaints = sorted(
            user_complaints, key=lambda x: x.timestamp, reverse=True
        )
        print(f"Found {len(sorted_complaints)} complaints for user")

        for complaint in sorted_complaints:
            print(f"  - {complaint.title}: {complaint.status.value}")

        return sorted_complaints

    def get_complaint_by_id(self, complaint_id: str) -> Optional[Complaint]:
        self.sync_from_backend()
        complaints = self._load_complaints()
        for complaint in complaints:
            if complaint.complaint_id == complaint_id:
                return complaint
        return None

    def get_all_complaints(self) -> List[Complaint]:
        self.sync_from_backend()
        return self._load_complaints()
