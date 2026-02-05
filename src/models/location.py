from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Location:
    latitude: float
    longitude: float
    timestamp: datetime = field(default_factory=datetime.now)
    accuracy: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "accuracy": self.accuracy,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Location":
        data = data.copy()
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

    def get_coordinates_string(self) -> str:
        return f"{self.latitude:.6f}, {self.longitude:.6f}"

    def is_valid(self) -> bool:
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180
