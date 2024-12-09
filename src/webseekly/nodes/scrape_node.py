from src.webseekly.core.node import Node
from playwright.sync_api import sync_playwright


class ScrapeNode(Node):
    def __init__(
        self, 
        input_key: list[str],       # ["crawled_data"]
        output_key: list[str],      # ["scraped_data"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        crawled_data = state.get(self.input_key[0])
        if not isinstance(crawled_data, list) or not all(isinstance(topic, list) for topic in crawled_data):
            raise ValueError(f"Invalid crawled_data format: {crawled_data}")

        scraped_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for topic_urls in crawled_data:  # トピックごとに処理
                topic_results = []
                for url_or_html in topic_urls:
                    try:
                        if url_or_html.startswith("http"):
                            page.goto(url_or_html)
                            page_content = page.content()
                            title = page.title()
                        else:
                            page_content = url_or_html
                            title = "No title"

                        links = [a.get_attribute('href') for a in page.query_selector_all('a')]

                        topic_results.append({
                            "title": title, 
                            "links": links
                        })
                    except Exception as e:
                        print(f"Error processing {url_or_html}: {e}")
                        continue
                scraped_data.append(topic_results)  # トピックごとの結果を保存

            browser.close()

        state[self.output_key[0]] = scraped_data
        return state
