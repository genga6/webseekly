import pytest
from unittest.mock import patch, AsyncMock
from src.webseekly.nodes.crawl_node import CrawlNode
from langgraph.graph import StateGraph
from typing import TypedDict

class State(TypedDict):
    url_data: dict

@pytest.mark.asyncio
async def test_crawl_node():
    """
    Test the CrawlNode functionality with mocked Playwright.
    """
    # Define input and output keys
    input_key = ["url_data"]
    output_key = ["url_data"]

    # Initialize CrawlNode
    crawl_node = CrawlNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("crawlnode", crawl_node)
    graph_builder.set_entry_point("crawlnode")
    graph_builder.set_finish_point("crawlnode")
    graph = graph_builder.compile()

    # Define initial state with mocked URLs
    state = {
        "url_data": {
            "https://example.com/1": {},
            "https://example.com/2": {}
        }
    }

    # Mock _fetch_url
    with patch.object(CrawlNode, "_fetch_url", new=AsyncMock()) as mock_fetch_url:
        # Simulate successful responses
        mock_fetch_url.side_effect = [
            "<html>Mocked Content 1</html>",
            "<html>Mocked Content 2</html>"
        ]

        # Execute the node
        result_state = await graph.ainvoke(state, debug=True)

        # Check if mock_fetch_url was called
        assert mock_fetch_url.call_count == 2, "_fetch_url should be called for each URL"

        # Assertions for crawled_data
        assert "url_data" in result_state, "State should contain 'url_data' key"
        assert "https://example.com/1" in result_state["url_data"], "URL data should include https://example.com/1"
        assert "https://example.com/2" in result_state["url_data"], "URL data should include https://example.com/2"

        assert result_state["url_data"]["https://example.com/1"].get("crawled_data", {}).get("content") == "<html>Mocked Content 1</html>", \
            "Crawled data for https://example.com/1 does not match expected content"

        assert result_state["url_data"]["https://example.com/2"].get("crawled_data", {}).get("content") == "<html>Mocked Content 2</html>", \
            "Crawled data for https://example.com/2 does not match expected content"
