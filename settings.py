from typing import Annotated, Optional

# Import dotenv for .env file support
from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    # LLM settings
    GEMINI_API_KEY: Annotated[SecretStr, Field(default_factory=lambda: SecretStr(""))] = SecretStr("")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash-exp")
    TEMPERATURE: float = Field(default=0.5)

    # OpenAI settings (optional)
    OPENAI_API_KEY: Annotated[SecretStr, Field(default_factory=lambda: SecretStr(""))] = SecretStr("")
    OPENAI_BASE_URL: Optional[str] = Field(default="")
    OPENAI_MODEL: str = Field(default="deepseek-chat")

    # DeepSeek settings (optional for compatibility with .env.example)
    DEEPSEEK_API_KEY: Annotated[SecretStr, Field(default_factory=lambda: SecretStr(""))] = SecretStr("")

    # Scraper settings
    WEBSITE_URL: str = Field(default="")
    OUTPUT_FILE: str = Field(default="data.txt")
    RESULTS_FILE: str = Field(default="results.txt")

    # Crew settings
    VERBOSE: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="debug")

    # Optional configuration
    AGENT_STREAM: bool = Field(default=True)
    AGENT_MARKDOWN: bool = Field(default=True)
    AGENT_SHOW_TOOL_CALLS: bool = Field(default=True)
    AGENT_MONITORING: bool = Field(default=True)

    DB_URL: str = Field(default="postgresql+psycopg://ai:ai@localhost:5532/ai")
    OLLAMA_HOST: str = Field(default="http://localhost:11434")
    HF_TOKEN: str = Field(default="")

    COHERE_API_KEY: str = Field(default="")
    COHERE_MODEL: str = Field(default="embed-multilingual-v3.0")
    COHERE_DIMENSIONS: int = Field(default=1024)

    @model_validator(mode="after")
    def check_api_keys(self) -> "Settings":
        """Validate that at least one API key is provided"""
        has_gemini = bool(self.GEMINI_API_KEY.get_secret_value())
        has_openai = bool(self.OPENAI_API_KEY.get_secret_value())
        has_deepseek = bool(self.DEEPSEEK_API_KEY.get_secret_value())

        if not (has_gemini or has_openai or has_deepseek):
            raise ValueError(
                "Either GEMINI_API_KEY, OPENAI_API_KEY, or DEEPSEEK_API_KEY must be set in environment variables"
            )

        # If DeepSeek key is provided but OpenAI key is not, use DeepSeek key for OpenAI
        if has_deepseek and not has_openai:
            self.OPENAI_API_KEY = self.DEEPSEEK_API_KEY

        return self

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, env_nested_delimiter="__", extra="ignore"
    )


settings = Settings()

__all__ = ["settings", "Settings"]
