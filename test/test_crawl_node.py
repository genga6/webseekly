import pytest
from unittest.mock import patch, Mock
from src.webseekly.nodes.crawl_node import CrawlNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    keywords: list[str]
    search_results: list[str]
    crawled_data: list[str]


def test_crawl_node():

    # Define input and output keys
    input_key = ["search_results"]
    output_key = ["crawled_data"]

    crawl_node = CrawlNode(input_key, output_key)

     # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("crawlnode", crawl_node)
    graph_builder.set_entry_point("crawlnode")
    graph_builder.set_finish_point("crawlnode")
    graph = graph_builder.compile()

    # Define initial state
    state = {
        "search_results": ["https://example.com/page1", "https://example.com/page2"],
        "crawled_data": [],
    }

    # Mock requests.get
    with patch("requests.get") as mock_get:
        # Simulate successful responses
        mock_get.return_value = Mock(status_code=200, text="Example Page Content")

        # Execute the node
        result_state = graph.invoke(state, debug=True)

        # Assertions
        assert "crawled_data" in result_state, "State should contain 'crawled_data' key"
        assert len(result_state["crawled_data"]) == 2, "Crawled data should have 2 entries"
        assert result_state["crawled_data"] == ["Example Page Content", "Example Page Content"], \
            "Crawled data does not match expected content"