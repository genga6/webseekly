import requests
from src.webseekly.core.node import Node


class CrawlNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["search_results"]
        output_key: list[str],  # ["crawled_data"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        """
        Executes the crawl operation for a single topic.
        Fetches HTML content for each URL in the 'search_results' list.
        """
        # Retrieve input data
        search_results = state.get(self.input_key[0], [])
        crawled_data = []

        for url in search_results:
            try:
                response = requests.get(url)
                response.raise_for_status()
                crawled_data.append(response.text)
            except requests.RequestException as e:
                print(f"Failed to crawl {url}: {e}")

        # Update state with the crawled data
        state[self.output_key[0]] = crawled_data

        return state
