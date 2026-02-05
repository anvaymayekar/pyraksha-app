import json
from typing import Any, Optional
from pathlib import Path
from src.config.app_config import AppConfig


class StorageService:
    _instance: Optional["StorageService"] = None

    def __init__(self):
        AppConfig.ensure_storage_dir()
        self._storage_dir = AppConfig.STORAGE_DIR

    @classmethod
    def get_instance(cls) -> "StorageService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _get_file_path(self, filename: str) -> Path:
        return self._storage_dir / filename

    def save(self, filename: str, data: Any) -> bool:
        try:
            file_path = self._get_file_path(filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Storage save error: {e}")
            return False

    def load(self, filename: str) -> Optional[Any]:
        try:
            file_path = self._get_file_path(filename)
            if not file_path.exists():
                return None
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Storage load error: {e}")
            return None

    def delete(self, filename: str) -> bool:
        try:
            file_path = self._get_file_path(filename)
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"Storage delete error: {e}")
            return False

    def exists(self, filename: str) -> bool:
        file_path = self._get_file_path(filename)
        return file_path.exists()
