import os
from pathlib import Path
from typing import Any


class Config:
    _instance = None
    _dictionary: dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            config_path = Path(__file__).parents[4] / "resources" / "urls.properties"

            if config_path.exists():
                with config_path.open(encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()

                        if not line or line.startswith("#"):
                            continue

                        if "=" in line:
                            key, value = line.split("=", maxsplit=1)
                            cls._dictionary[key.strip()] = value.strip()

        return cls._instance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        Config()

        env_key = Config._to_env_key(key)

        return os.getenv(env_key, Config._dictionary.get(key, default_value))

    @staticmethod
    def require(key: str) -> str:
        value = Config.fetch(key)

        if value is None or value == "":
            env_key = Config._to_env_key(key)
            raise RuntimeError(
                f"Required setting is missing: {key}. "
                f"Set {env_key} or add it to resources/urls.properties."
            )

        return value

    @staticmethod
    def _to_env_key(key: str) -> str:
        result = ""

        for char in key:
            if char.isupper():
                result += "_" + char
            else:
                result += char.upper()

        return result
