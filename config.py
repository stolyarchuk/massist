from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    # LLM settings
    DEEPSEEK_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = ""
    HUGGINGFACE_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = ""
    GEMINI2_MODEL: str = ""
    GEMINI_EMBED_MODEL: str = ""
    VLLM_MODEL: str = ""
    VLLM_API_KEY: str = ""

    VLLM0_BASE_URL: str = ""
    VLLM1_BASE_URL: str = ""

    # Scraper settings
    WEBSITE_URL: str = ""

    # Optional configuration
    AGENT_STREAM: bool = True
    AGENT_MARKDOWN: bool = True
    AGENT_SHOW_TOOL_CALLS: bool = True
    AGENT_MONITORING: bool = False
    AGENT_DEBUG: bool = False

    TEAM_DEBUG: bool = True

    POSTGRES_URL: str = ""
    MONGO_URL: str = ""

    MAX_TOKENS: int = 5000
    MAX_LINKS: int = 10
    DIMS: int = 1024
    VECTOR_DB: str = ""
    STORAGE_DB: str = ""
    MEMORY_DB: str = ""
    LOG_LEVEL = 'debug'
    TEMPERATURE = 0.5
    ALLOW_ORIGINS = '*'

    @model_validator(mode="after")
    def check_api_keys(self) -> "Config":
        """Validate that at least one API key is provided"""
        has_gemini = bool(self.GOOGLE_API_KEY)
        has_deepseek = bool(self.DEEPSEEK_API_KEY)

        if not (has_gemini or has_deepseek):
            raise ValueError(
                "Either GEMINI_API_KEY or DEEPSEEK_API_KEY must be set in environment variables"
            )

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter="__",
        extra="ignore"
    )


config = Config()

__all__ = ["config"]
