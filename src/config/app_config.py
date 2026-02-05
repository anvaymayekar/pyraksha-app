from pathlib import Path


class AppConfig:
    APP_NAME = "PyRaksha"
    APP_VERSION = "1.0.0"

    API_BASE_URL = "http://127.0.0.1:5000"
    STORAGE_DIR = Path.home() / ".pyraksha"
    USERS_FILE = "users.json"
    COMPLAINTS_FILE = "complaints.json"
    SOS_HISTORY_FILE = "sos_history.json"
    SESSION_FILE = "session.json"
    ACTIVE_SOS_FILE = "active_sos.json"

    SOS_LOCATION_UPDATE_INTERVAL = 10
    SESSION_TIMEOUT_DAYS = 30

    @classmethod
    def ensure_storage_dir(cls) -> None:
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
