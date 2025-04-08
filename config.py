from typing import Any, List

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    # LLM settings
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL_PRI: str = ""
    GOOGLE_MODEL_SEC: str = ""
    GOOGLE_MODEL_EMBED: str = ""

    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = ""

    VLLM_API_KEY: str = ""
    VLLM_MODEL: str = ""
    VLLM_MODEL_EMBED: str = ""
    VLLM_BASE_URL_PRI: str = ""
    VLLM_BASE_URL_SEC: str = ""

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = ""

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_EMBED: str = ""

    HUGGINGFACE_API_KEY: str = ""

    LLMX_API_KEY: str = ""

    WEBSITE_URL: str = ""

    TGBOT_API_TOKEN: str = ""
    TGBOT_CHAT_ID: str = ""

    # Optional configuration
    AGENT_STREAM: bool = True
    AGENT_MARKDOWN: bool = True
    AGENT_SHOW_TOOL_CALLS: bool = True
    AGENT_MONITORING: bool = False
    AGENT_DEBUG: bool = False

    TEAM_DEBUG: bool = True

    # ThinkingTools configuration
    THINKING_TOOLS_ENABLE: bool = False
    THINKING_TOOLS_ADD_INSTRUCTIONS: bool = False

    POSTGRES_URL: str = ""
    MONGO_URL: str = ""
    SQLITE_URL: str = ""
    DBLANCE_URL: str = ""
    REDIS_URL: str = ""

    VECTOR_DB: str = ""
    VECTOR_SEARCH: str = "vector"
    STORAGE_DB: str = ""
    MEMORY_DB: str = ""

    MAX_CHUNK_SIZE: int = 5000
    MAX_TOKENS: int = 40000
    MAX_LINKS: int = 10
    MAX_DEPTH: int = 4
    DIMS: int = 1024
    LOG_LEVEL: str = "debug"
    TEMPERATURE: float = 0.5
    ALLOW_ORIGINS: List[str] = Field(default=["localhost", "127.0.0.1"])
    CHUNKING_STRATEGY: str = "agentic"
    CACHE_TTL: int = 86400

    CHAT_IDX_NAME: str = ""
    CHAT_IDX_PREFIX: str = ""

    @field_validator("ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_env_lists(cls, value: Any) -> List[str]:
        if isinstance(value, str):
            # Strip whitespace and filter out empty strings
            return [item.strip() for item in value.split(",") if item.strip()]

        return value

    @model_validator(mode="after")
    def check_api_keys(self) -> "Config":
        """Validate that at least one API key is provided"""

        if not self.GOOGLE_API_KEY:
            raise ValueError(
                "MAI_GOOGLE_API_KEY must be set in environment variables")

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="MAI_",
        # env_nested_delimiter="__",
        extra="ignore",
    )


config = Config()

__all__ = ["config"]
