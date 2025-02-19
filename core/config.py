from pydantic_settings import BaseSettings, SettingsConfigDict

class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")

class DBSettings(Base):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class BotSettings(Base):
    BOT_TOKEN: str
    
class JiraSettings(Base):
    JIRA_URL: str
    JIRA_TOKEN: str

class Settings:
    DB: DBSettings = DBSettings()
    BOT: BotSettings = BotSettings()
    JIRA: JiraSettings = JiraSettings()

settings = Settings()