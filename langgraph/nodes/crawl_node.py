import requests
from typing import TypedDict

class State(TypedDict):
    keywords: list[str]
    search_results: list[str]
    crawled_data: list[str]

class CrawlNode:
    def __init__(self):
        pass

    def __call__(self, state: State) -> dict:
        # "search_results"から各リンクのHTMLデータを取得
        search_results = state.get("search_results", [])
        crawled_data = []

        for url in search_results:
            try:
                response = requests.get(url)
                response.raise_for_status
                crawled_data.append(response.text)
            except requests.RequestException as e:
                print(f"Failed to crawl {url}: {e}")

        state["crawled_data"] = crawled_data
        return state
    
if __name__ == "__main__":
    crawl_node = CrawlNode()
    initial_state = {
        "search_results": [
            "https://example.com/search?q=AIの技術",
            "https://example.com/search?q=最新のAI"
        ]
    }
    updated_state = crawl_node(initial_state)
    print("Updated State:", updated_state)