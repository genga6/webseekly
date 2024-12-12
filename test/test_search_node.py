import pytest
from unittest.mock import patch, AsyncMock
from src.webseekly.nodes.search_node import SearchNode
from langgraph.graph import StateGraph
from typing import TypedDict

class State(TypedDict):
    queries: list[str]
    url_data: dict

@pytest.mark.asyncio
async def test_search_node():
    """
    Test the SearchNode functionality with mocked Google Custom Search API.
    """
    # Define input and output keys
    input_key = ["queries"]
    output_key = ["url_data"]

    # Initialize SearchNode
    search_node = SearchNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("searchnode", search_node)
    graph_builder.set_entry_point("searchnode")
    graph_builder.set_finish_point("searchnode")
    graph = graph_builder.compile()

    # Define initial state
    state = {
        "queries": ["AIの技術", "最新のAI"],
        "url_data": {}
    }

    # Mock _search_google
    with patch.object(SearchNode, "_search_google", new=AsyncMock()) as mock_search_google:
        # Simulate API responses
        mock_search_google.side_effect = [
            [
                {"query": "AIの技術", "title": "Result 1", "link": "https://example.com/1", "snippet": "Snippet 1"},
                {"query": "AIの技術", "title": "Result 2", "link": "https://example.com/2", "snippet": "Snippet 2"}
            ],
            [
                {"query": "最新のAI", "title": "Result 3", "link": "https://example.com/3", "snippet": "Snippet 3"}
            ]
        ]

        # Execute the node
        result_state = await graph.ainvoke(state, debug=True)

        # Check if mock_search_google was called
        assert mock_search_google.call_count == 2, "_search_google should be called for each query"

        # Assertions for url_data
        assert "url_data" in result_state, "State should contain 'url_data' key"

        assert "https://example.com/1" in result_state["url_data"], "URL data should include https://example.com/1"
        assert result_state["url_data"]["https://example.com/1"]["search_results"]["title"] == "Result 1", \
            "Search results for https://example.com/1 do not match expected content"

        assert "https://example.com/2" in result_state["url_data"], "URL data should include https://example.com/2"
        assert result_state["url_data"]["https://example.com/2"]["search_results"]["title"] == "Result 2", \
            "Search results for https://example.com/2 do not match expected content"

        assert "https://example.com/3" in result_state["url_data"], "URL data should include https://example.com/3"
        assert result_state["url_data"]["https://example.com/3"]["search_results"]["title"] == "Result 3", \
            "Search results for https://example.com/3 do not match expected content"
