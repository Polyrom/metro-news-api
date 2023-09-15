from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    host: str
    port: int
    sqlite_db: str

    model_config = SettingsConfigDict(env_file='.env')


@cache
def get_settings() -> ProjectSettings:
    """
    Factory function for project settings
    """
    return ProjectSettings()
