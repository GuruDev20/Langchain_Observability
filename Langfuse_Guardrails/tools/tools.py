from langchain.tools import Tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    results = client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    formatted = []
    for r in results.get("results", []):
        formatted.append(f"{r['title']}\n{r['url']}\n{r['content']}\n")

    return "\n---\n".join(formatted)

web_search_tool = Tool(
    name="web_search",
    func=web_search,
    description="Search the web using Tavily for real-time and reliable information"
)
