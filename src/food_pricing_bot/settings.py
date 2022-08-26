import logging
import os
import traceback
from functools import lru_cache
from pathlib import PurePosixPath

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    TOKEN: str
    DATA_PATH: str

    class Config:
        env_file = ".env"

    @validator("DATA_PATH")
    def validate_path(cls, v: str) -> str:
        try:
            path = PurePosixPath(v)
        except Exception:
            logging.error(traceback.format_exc())
            raise ValueError("Failed transformation of path in PurePosixPath.")
        # check that the path exists
        if not os.path.isdir(path):
            raise ValueError("Data path not found.")
        return path


@lru_cache()
def get_settings() -> Settings:
    return Settings()
