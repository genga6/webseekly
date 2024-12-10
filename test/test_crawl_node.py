import pytest
from unittest.mock import patch, AsyncMock
from src.webseekly.nodes.crawl_node import CrawlNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    search_results: list[str]
    crawled_data: list[str]

@pytest.mark.asyncio
async def test_crawl_node():
    """
    Test the CrawlNode functionality with mocked Playwright.
    """
    # Define input and output keys
    input_key = ["search_results"]
    output_key = ["crawled_data"]

    # Initialize CrawlNode
    crawl_node = CrawlNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("crawlnode", crawl_node)
    graph_builder.set_entry_point("crawlnode")
    graph_builder.set_finish_point("crawlnode")
    graph = graph_builder.compile()

    # Define initial state for a single topic
    state = {
        "search_results": ["https://example.com/page1", "https://example.com/page2"],  # Mocked URLs
        "crawled_data": [],
    }

    # Mock _fetch_url
    with patch.object(CrawlNode, "_fetch_url", new=AsyncMock()) as mock_fetch_url:
        # Simulate successful responses
        mock_fetch_url.side_effect = ["Mocked Page Content 1", "Mocked Page Content 2"]
        
        print("Mock has been set up!")
        print(f"Mock call count before invoke: {mock_fetch_url.call_count}")

        # Execute the node
        result_state = await graph.ainvoke(state, debug=True)

        # Check if mock_fetch_url was called
        print(f"Mock call count after invoke: {mock_fetch_url.call_count}")

        # Assertions
        assert "crawled_data" in result_state, "State should contain 'crawled_data' key"
        assert len(result_state["crawled_data"]) == 2, "Crawled data should have 2 entries"
        assert result_state["crawled_data"] == ["Mocked Page Content 1", "Mocked Page Content 2"], \
            "Crawled data does not match expected content"
