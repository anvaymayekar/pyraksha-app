from datetime import datetime, timedelta
from typing import Optional


class DateTimeHelper:
    @staticmethod
    def format_timestamp(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(format_string)

    @staticmethod
    def format_date_friendly(dt: datetime) -> str:
        now = datetime.now()
        delta = now - dt

        if delta.days == 0:
            if delta.seconds < 60:
                return "Just now"
            elif delta.seconds < 3600:
                minutes = delta.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                hours = delta.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.days == 1:
            return "Yesterday"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        else:
            return dt.strftime("%b %d, %Y")

    @staticmethod
    def format_duration(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    @staticmethod
    def is_recent(dt: datetime, hours: int = 24) -> bool:
        now = datetime.now()
        delta = now - dt
        return delta < timedelta(hours=hours)

    @staticmethod
    def parse_iso(iso_string: str) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(iso_string)
        except (ValueError, TypeError):
            return None
