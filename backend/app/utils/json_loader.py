import json
import os
import logging

logger = logging.getLogger(__name__)

class JSONLoader:
    _schemes_data = None

    @classmethod
    def load_schemes(cls) -> list[dict]:
        if cls._schemes_data is not None:
            return cls._schemes_data

        filepath = os.path.join(os.path.dirname(__file__), "..", "data", "schemes.json")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                cls._schemes_data = json.load(f)
            logger.info("Loaded schemes data into memory.")
        except Exception as e:
            logger.error(f"Failed to load schemes.json: {e}")
            cls._schemes_data = []

        return cls._schemes_data
