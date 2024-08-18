from langchain_community.tools.tavily_search import TavilySearchResults

# https://tavily.com/


def get_profile_url_tavily(name: str):
    """Search for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]
