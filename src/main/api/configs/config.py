from pathlib import Path
from typing import Any


class Config:
    _instance = None
    _dictionary: dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            config_path = Path(__file__).parents[4] / "resources" / "urls.properties"

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with config_path.open(encoding="utf-8") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.split("=", maxsplit=1)
                        cls._dictionary[key.strip()] = value.strip()

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        Config()
        return Config._dictionary.get(key, default_value)
