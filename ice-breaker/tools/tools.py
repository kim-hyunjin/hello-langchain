from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Search for Linkedin  Profile Page."""
    # https://tavily.com/ 에서 만든 툴을 사용하면 구글에서 크롤링해 원하는 url을 찾을 수 있음.
    # TAVILY_API_KEY 필요
    # search = TavilySearchResults()
    # res = search.run(f"{name}")
    # return res[0]["url"]
    return f"https://www.linkedin.com/in/{name}/"
