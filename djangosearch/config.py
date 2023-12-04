from secrets import token_hex
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='search_')
    debug: bool = True
    secret_key: str = Field(default_factory=lambda: token_hex(28))
    allowed_hosts: list[HttpUrl] = Field(default_factory=list)
    db_name: str = 'starwars'
    db_user: str = 'postgres'
    db_password: str = 'hum'
    db_host: str = 'localhost'
    db_port: int = 5432
    csrf_cookie_secure: bool = False
    session_cookie_secure: bool = False
