from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    MAX_TOKENS: int = 5000
    MAX_LINKS: int = 10
    DIMS: int = 1024
    VECTOR_DB: str = ""
    STORAGE_DB: str = ""
    MEMORY_DB: str = ""

    # LLM settings
    DEEPSEEK_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = ""
    GEMINI2_MODEL: str = ""
    GEMINI_EMBED_MODEL: str = ""
    VLLM_MODEL: str = ''

    TEMPERATURE: float = 0.5

    # OpenAI settings (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = ""

    # Scraper settings
    WEBSITE_URL: str = ""
    ALLOW_ORIGINS: str = '*'

    # Crew settings
    LOG_LEVEL: str = "debug"

    # Optional configuration
    AGENT_STREAM: bool = True
    AGENT_MARKDOWN: bool = True
    AGENT_SHOW_TOOL_CALLS: bool = False
    AGENT_MONITORING: bool = True
    AGENT_DEBUG: bool = False

    TEAM_DEBUG: bool = True

    POSTGRES_URL: str = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    MONGO_URL: str = "mongodb://192.168.31.240:27017"

    OLLAMA0_HOST: str = "http://localhost:11434"
    OLLAMA1_HOST: str = "http://localhost:11435"

    @model_validator(mode="after")
    def check_api_keys(self) -> "Config":
        """Validate that at least one API key is provided"""
        has_gemini = bool(self.GOOGLE_API_KEY)
        has_openai = bool(self.OPENAI_API_KEY)
        has_deepseek = bool(self.DEEPSEEK_API_KEY)

        if not (has_gemini or has_openai or has_deepseek):
            raise ValueError(
                "Either GEMINI_API_KEY, OPENAI_API_KEY, or DEEPSEEK_API_KEY must be set in environment variables"
            )

        # If DeepSeek key is provided but OpenAI key is not, use DeepSeek key for OpenAI
        if has_deepseek and not has_openai:
            self.OPENAI_API_KEY = self.DEEPSEEK_API_KEY

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
