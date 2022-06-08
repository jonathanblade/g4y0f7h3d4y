from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field(default="Gay of the day", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=3000, env="APP_PORT")

    api_prefix: str = Field(default="/api", env="API_PREFIX")
    docs_url: str | None = Field(default="/docs", env="DOCS_URL")
    redoc_url: str | None = Field(default=None, env="REDOC_URL")

    debug_mode: bool = Field(default=False, env="DEBUG_MODE")

    db_user: str = Field(default="root", env="DB_USER")
    db_password: str = Field(default="root", env="DB_PASSWORD")
    db_name: str = Field(default="main", env="DB_NAME")

    @property
    def db_url(cls) -> str:
        return f"mongodb+srv://{cls.db_user}:{cls.db_password}@cluster0.knywm.mongodb.net/?retryWrites=true&w=majority"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SETTINGS = Settings()
