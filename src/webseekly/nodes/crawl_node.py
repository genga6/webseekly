import asyncio
from playwright.async_api import async_playwright
from src.webseekly.core.node import Node


class CrawlNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["search_results"]
        output_key: list[str],  # ["crawled_data"]
    ):
        super().__init__(input_key, output_key)

    async def _execute_async(self, state: dict) -> dict:
        try:
            # Retrieve input data
            search_results = state.get(self.input_key[0])
            if not search_results:
                print("No search results found in state.")
                return state

            # Prepare and execute tasks
            tasks = [self._fetch_url(url) for url in search_results]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            crawled_data = [
                result if isinstance(result, str) else f"Error: {result}"
                for result in results
            ]

            # Update state with the crawled data
            state[self.output_key[0]] = crawled_data
            print(f"Updated State: {state}")

        except Exception as e:
            print(f"Exception occurred in _execute_async: {e}")

        print("Finished _execute_async")
        return state

    async def _fetch_url(self, url: str) -> str:
        """
        Fetches the HTML content of a URL using Playwright.
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
        Wrapper to execute the asynchronous logic in a synchronous manner.
        """
        
        try:
            # 現在のイベントループを取得
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # イベントループが存在しない場合は新規作成
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # 非同期メソッドを同期的に実行
        return loop.run_until_complete(self._execute_async(state))