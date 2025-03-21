from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration settings class that reads values from environment variables.
    Environment variables can be loaded from .env files using python-dotenv.
    """

    MAX_LINKS: int = 1000

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
    DEEPSEEK_API_KEY: str = ""

    # Scraper settings
    WEBSITE_URL: str = ""
    OUTPUT_FILE: str = "data.txt"
    RESULTS_FILE: str = "results.txt"

    # Crew settings
    VERBOSE: bool = True
    LOG_LEVEL: str = "debug"

    # Optional configuration
    AGENT_STREAM: bool = True
    AGENT_MARKDOWN: bool = True
    AGENT_SHOW_TOOL_CALLS: bool = False
    AGENT_MONITORING: bool = True

    DB_URL: str = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    MONGO_URL: str = "mongodb://192.168.31.240:27017"

    OLLAMA0_HOST: str = "http://localhost:11434"
    OLLAMA1_HOST: str = "http://localhost:11435"
    HUGGINGFACE_API_KEY: str = ""

    COHERE_API_KEY: str = ""
    COHERE_MODEL: str = "embed-multilingual-v3.0"
    COHERE_DIMENSIONS: int = 1024

    FIRECRAWL_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

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
