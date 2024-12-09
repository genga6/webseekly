from src.webseekly.core.node import Node
from playwright.sync_api import sync_playwright


class ScrapeNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["crawled_data"]
        output_key: list[str],  # ["scraped_data"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        """
        Executes the scrape operation for a single topic.
        Extracts links and titles from crawled HTML data or URLs.
        """
        crawled_data = state.get(self.input_key[0])
        if not isinstance(crawled_data, list) or not all(isinstance(item, str) for item in crawled_data):
            raise ValueError(f"Invalid crawled_data format: {crawled_data}")

        scraped_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for url_or_html in crawled_data:
                try:
                    if url_or_html.startswith("http"):
                        # URL is provided
                        page.goto(url_or_html)
                        page_content = page.content()
                        title = page.title()
                    else:
                        # HTML content is provided
                        page_content = url_or_html
                        title = "No title"

                    links = [a.get_attribute('href') for a in page.query_selector_all('a')]

                    scraped_data.append({
                        "title": title, 
                        "links": links
                    })
                except Exception as e:
                    print(f"Error processing {url_or_html}: {e}")
                    continue

            browser.close()

        # Update state with the scraped data
        state[self.output_key[0]] = scraped_data
        return state
