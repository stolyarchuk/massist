from typing import Annotated, Optional

# Import dotenv for .env file support
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    # LLM settings
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_EMBED_MODEL: str = "gemini-embedding-exp-03-07"
    TEMPERATURE: float = 0.5

    # OpenAI settings (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = ""

    # DeepSeek settings (optional for compatibility with .env.example)
    DEEPSEEK_API_KEY: str = Field(default="")

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
    AGENT_SHOW_TOOL_CALLS: bool = Field(default=False)
    AGENT_MONITORING: bool = Field(default=True)

    DB_URL: str = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    OLLAMA0_HOST: str = "http://localhost:11434"
    OLLAMA1_HOST: str = "http://localhost:11435"
    HUGGINGFACE_API_KEY: str = ""

    COHERE_API_KEY: str = Field(default="")
    COHERE_MODEL: str = Field(default="embed-multilingual-v3.0")
    COHERE_DIMENSIONS: int = Field(default=1024)

    FIRECRAWL_API_KEY: str = Field(default="")
    OPENROUTER_API_KEY: str = Field(default="")

    @model_validator(mode="after")
    def check_api_keys(self) -> "Settings":
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


settings = Settings()

__all__ = ["settings"]
