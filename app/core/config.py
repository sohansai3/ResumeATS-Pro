from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Resume ATS Score Analyzer"
    database_url: str = "sqlite:///./ats_analyzer.db"
    log_level: str = "INFO"
    max_upload_mb: int = 8
    report_dir: str = "reports"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def ensure_directories(self) -> None:
        Path("app/logs").mkdir(parents=True, exist_ok=True)
        Path(self.report_dir).mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
