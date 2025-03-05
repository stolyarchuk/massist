from crewai import LLM, Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool

from settings import Settings

# Load settings from environment variables
settings = Settings()


# Determine which LLM to use based on available API keys
# if settings.gemini_api_key.get_secret_value():
llm = LLM(
    model="openai/deepseek-chat",
    api_base=settings.OPENAI_BASE_URL,
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    temperature=0.5,
    # max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42,
)
# elif settings.openai_api_key.get_secret_value() or settings.deepseek_api_key.get_secret_value():
# llm = ChatOpenAI(
#     model=settings.openai_model,
#     base_url=settings.openai_base_url,
#     api_key=settings.openai_api_key,
#     temperature=settings.temperature,
#     verbose=settings.verbose,
# )

# llm = ChatDeepSeek(
#     model=settings.openai_model,
#     # base_url=settings.openai_base_url,
#     api_key=settings.deepseek_api_key.get_secret_value(),
#     temperature=settings.temperature,
#     verbose=settings.verbose,
# )
# else:
# raise ValueError("No API key available for LLM services")

# Instantiate tools
web_scrape_tool = ScrapeWebsiteTool(website_url=settings.WEBSITE_URL)

# Create agents
web_scraper_agent = Agent(
    role="Web Scraper",
    goal="Effectively Scrape data on the websites for your company",
    backstory="""You are expert web scraper, your job is to scrape all the data for
                your company from a given website.
                """,
    tools=[web_scrape_tool],
    verbose=settings.VERBOSE,
    llm=llm,
)

# Define tasks
web_scraper_task = Task(
    description="Scrape all the data on the site so your company can use for decision making.",
    expected_output="All the content of the website.",
    agent=web_scraper_agent,
    output_file=settings.OUTPUT_FILE,
)

# Assemble a crew
crew = Crew(
    agents=[web_scraper_agent],
    tasks=[web_scraper_task],
    verbose=settings.VERBOSE,
)

# Execute tasks
result = crew.kickoff()
# print(result)

with open(settings.RESULTS_FILE, "w") as f:
    f.write(str(result))
