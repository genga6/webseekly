from src.webseekly.core.node import Node
from playwright.sync_api import sync_playwright


class ScrapeNode(Node):
    def __init__(
        self, 
        input_key: list[str],       # [crawled_data"]
        output_key: list[str],      # ["scraped_data"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        
        crawled_data = state.get(self.input_key[0])
        if not crawled_data:
            raise ValueError(f"No data found for input_key: {self.input_key[0]}")
        
        scraped_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for url_or_html in crawled_data:
                if url_or_html.startswith("http"):
                    page.goto(url_or_html)
                    page_content = page.content()
                else:
                    page_content = url_or_html

                title = page.title() if url_or_html.startswith("http") else "No title"
                links = [a.get_attributes('href') for a in page.query_selector_all('a')]

                extracted_data = {
                    "title": title, 
                    "links": links
                }
                scraped_data.append(extracted_data)

            browser.close()

        state[self.output_key[0]] = scraped_data
        return state