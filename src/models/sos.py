from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from src.config.constants import SOSStatus
from src.models.location import Location


@dataclass
class SOS:
    sos_id: str
    user_id: str
    status: SOSStatus
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    location_history: List[Location] = field(default_factory=list)

    def activate(self) -> None:
        self.status = SOSStatus.ACTIVE
        self.start_time = datetime.now()
        self.end_time = None

    def resolve(self) -> None:
        self.status = SOSStatus.RESOLVED
        self.end_time = datetime.now()

    def add_location(self, location: Location) -> None:
        if self.status == SOSStatus.ACTIVE:
            self.location_history.append(location)

    def get_duration_seconds(self) -> int:
        if self.end_time:
            delta = self.end_time - self.start_time
        else:
            delta = datetime.now() - self.start_time
        return int(delta.total_seconds())

    def get_latest_location(self) -> Optional[Location]:
        return self.location_history[-1] if self.location_history else None

    def to_dict(self) -> dict:
        return {
            "sos_id": self.sos_id,
            "user_id": self.user_id,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "location_history": [loc.to_dict() for loc in self.location_history],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SOS":
        data = data.copy()
        data["status"] = SOSStatus(data["status"])
        if "start_time" in data and isinstance(data["start_time"], str):
            data["start_time"] = datetime.fromisoformat(data["start_time"])
        if data.get("end_time") and isinstance(data["end_time"], str):
            data["end_time"] = datetime.fromisoformat(data["end_time"])
        if "location_history" in data:
            data["location_history"] = [
                Location.from_dict(loc) for loc in data["location_history"]
            ]
        return cls(**data)
