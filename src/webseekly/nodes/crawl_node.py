import requests
from src.webseekly.core.node import Node


class CrawlNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str],
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        # "search_results"から各リンクのHTMLデータを取得
        search_results = state.get(self.input_key[0])
        crawled_data = state.get(self.output_key[0], [])

        for url in search_results:
            try:
                response = requests.get(url)
                response.raise_for_status
                crawled_data.append(response.text)
            except requests.RequestException as e:
                print(f"Failed to crawl {url}: {e}")

        state[self.output_key[0]] = crawled_data
        
        return state