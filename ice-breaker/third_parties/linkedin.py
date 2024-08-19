import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from LinkedIn profiles
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        """
        TODO: use proxycurl api or scrape linkedin profile myself
        """
        raise Exception("sorry, not implemendted yet")

    data = response.json()

    # 토큰 개수를 줄이기 위해 필요없는 데이터 없애기
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ("people_also_viewed", "certifications")
    }

    # temp - 위에서 가져온 url은 이미지가 보이지않아 아래 url 수정
    data["profile_pic_url"] = (
        "https://img-c.udemycdn.com/user/200_H/30508036_0f4a_4.jpg"
    )

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-macro", mock=True
        )
    )
