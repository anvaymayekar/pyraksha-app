from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from src.config.constants import ComplaintStatus


@dataclass
class Complaint:
    complaint_id: str
    user_id: str
    title: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: ComplaintStatus = ComplaintStatus.PENDING
    resolution_notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "complaint_id": self.complaint_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "resolution_notes": self.resolution_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Complaint":
        data = data.copy()
        data["status"] = ComplaintStatus(data["status"])
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

    def get_status_display(self) -> str:
        return self.status.value.replace("_", " ").title()

    def get_formatted_date(self) -> str:
        return self.timestamp.strftime("%b %d, %Y at %I:%M %p")
