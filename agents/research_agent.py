
from tavily import TavilyClient
from config.settings import TAVILY_API_KEY, MAX_SEARCH_RESULTS


def research(topic: str) -> list[dict]:
    """
    Search the web and collect relevant research findings.
    """

    # Step 1: Validate API key
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is missing in .env")

    # Step 2: Initialize Tavily
    client = TavilyClient(api_key=TAVILY_API_KEY)

    # Step 3: Search the internet
    response = client.search(
        query=topic,
        search_depth="advanced",
        max_results=MAX_SEARCH_RESULTS,
        include_answer=False
    )

    # Step 4: Extract search results
    results = response.get("results", [])

    # Step 5: Check search results
    if not results:
        raise ValueError("No research results found.")

    # Step 6: Structure the information
    findings = []

    for item in results:

        finding = {
            "title": item.get("title", "Untitled"),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0)
        }

        findings.append(finding)

    # Step 7: Return findings
    return findings
