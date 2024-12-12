import asyncio
from playwright.async_api import async_playwright
from src.webseekly.core.node import Node

class CrawlNode(Node):
    def __init__(
        self,
        input_key: list[str],  # ["url_data"]
        output_key: list[str],  # ["url_data"]
    ):
        super().__init__(input_key, output_key)

    async def _execute_async(self, state: dict) -> dict:
        """
        Crawls URLs in the url_data and updates their crawled_data field.

        Args:
            state (dict): Input state containing the url_data.

        Returns:
            dict: Updated state with crawled content.
        """
        url_data = state.get(self.input_key[0], {})
        if not url_data:
            print("No URL data found in state.")
            return state

        # Prepare and execute crawling tasks
        tasks = [
            self._fetch_url(url) for url in url_data.keys()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Update url_data with the crawled content
        for url, result in zip(url_data.keys(), results):
            if isinstance(result, str):
                url_data[url]["crawled_data"] = {"content": result}
            else:
                url_data[url]["crawled_data"] = {"error": str(result)}

        state[self.output_key[0]] = url_data
        return state

    async def _fetch_url(self, url: str) -> str:
        """
        Fetches the HTML content of a URL using Playwright.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
            return ""

    def execute(self, state: dict) -> dict:
        """
        Synchronous wrapper to execute the asynchronous logic.

        Args:
            state (dict): Input state containing the url_data.

        Returns:
            dict: Updated state with crawled content.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self._execute_async(state))
