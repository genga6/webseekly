import httpx
import asyncio
from src.webseekly.core.node import Node

class SearchNode(Node):
    def __init__(
        self,
        input_key: list[str],  # ["queries"]
        output_key: list[str],  # ["url_data"]
        google_api_key: str, 
        search_engine_id: str
    ):
        super().__init__(input_key, output_key)
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id

        if not self.google_api_key or not self.search_engine_id:
            raise EnvironmentError("API_KEY or SEARCH_ENGINE_ID is not set in the environment.")

    async def _execute_async(self, state) -> dict:
        """
        Executes the search operation using Google Custom Search API asynchronously.

        Args:
            state (dict): Input state containing the search queries.

        Returns:
            dict: Updated state with search results in url_data.
        """
        queries = state.get(self.input_key[0], [])
        if not isinstance(queries, list) or not queries:
            raise ValueError("A list of queries is required for SearchNode.")

        url_data = state.get(self.output_key[0], {})
        num_results = state.get("num_results", 10)

        # Execute the search for each query and collect results
        search_results = await self._search_multiple_queries(queries, num_results)

        # Populate url_data
        for result in search_results:
            url = result["link"]
            if url not in url_data:
                url_data[url] = {
                    "queries": [],
                    "search_results": result,
                }
            if result["query"] not in url_data[url]["queries"]:
                url_data[url]["queries"].append(result["query"])

        state[self.output_key[0]] = url_data
        return state

    async def _search_multiple_queries(self, queries: list, num_results: int) -> list[dict]:
        """
        Executes multiple queries asynchronously using Google Custom Search API.

        Args:
            queries (list): List of search queries.
            num_results (int): Number of results per query.

        Returns:
            list[dict]: A flat list of search results.
        """
        async with httpx.AsyncClient() as client:
            tasks = [
                self._search_google(client, query, num_results)
                for query in queries
            ]
            results = await asyncio.gather(*tasks)

            # Flatten the results
            return [item for result in results for item in result]

    async def _search_google(self, client: httpx.AsyncClient, query: str, num_results: int) -> list[dict]:
        """
        Performs a single Google Custom Search API call asynchronously.

        Args:
            client (httpx.AsyncClient): HTTP client instance.
            query (str): The search query.
            num_results (int): Number of results to retrieve.

        Returns:
            list[dict]: A list of search result objects.
        """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": num_results,
        }
        response = await client.get(url, params=params)

        if response.status_code != 200:
            raise RuntimeError(f"Google Custom Search API error: {response.status_code} - {response.text}")

        results = response.json().get("items", [])
        return [
            {
                "query": query,
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet"),
            }
            for result in results
        ]

    def execute(self, state) -> dict:
        """
        Synchronous wrapper to execute the asynchronous logic.

        Args:
            state (dict): Input state containing the search queries.

        Returns:
            dict: Updated state with search results in url_data.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self._execute_async(state))
