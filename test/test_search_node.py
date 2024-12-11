import pytest
from unittest.mock import patch, AsyncMock
from src.webseekly.nodes.search_node import SearchNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    queries: list[str]
    search_results: list[dict]

@pytest.mark.asyncio
async def test_search_node():
    """
    Test the SearchNode functionality with multiple queries.
    """
    # Define input and output keys
    input_key = ["queries"]
    output_key = ["search_results"]

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
        "queries": ["AIの技術", "最新のAI", "AIのトレンド"],
        "search_results": [],
    }

    # Mock SearchNode's _search_google method
    mock_results = [
        {"query": "AIの技術", "title": "Result 1", "link": "https://example.com/1", "snippet": "Snippet 1"},
        {"query": "最新のAI", "title": "Result 2", "link": "https://example.com/2", "snippet": "Snippet 2"},
        {"query": "AIのトレンド", "title": "Result 3", "link": "https://example.com/3", "snippet": "Snippet 3"},
    ]

    async def mock_search(client, query, num_results):
        for result in mock_results:
            if result["query"] == query:
                return [result]  # 返り値をリストでラップ
        return []

    with patch.object(SearchNode, "_search_google", new=AsyncMock(side_effect=mock_search)) as mock_search_google:
        # Log before execution
        print(f"Initial state: {state}")

        # Execute the graph
        result_state = await graph.ainvoke(state, debug=True)

        # Log after execution
        print(f"Result state: {result_state}")

    # Expected search results
    expected_results = [
        {"query": "AIの技術", "title": "Result 1", "link": "https://example.com/1", "snippet": "Snippet 1"},
        {"query": "最新のAI", "title": "Result 2", "link": "https://example.com/2", "snippet": "Snippet 2"},
        {"query": "AIのトレンド", "title": "Result 3", "link": "https://example.com/3", "snippet": "Snippet 3"},
    ]

    # Assertions
    assert result_state["search_results"] == expected_results, "Search results do not match expected output"
    assert "queries" in result_state, "State should retain the 'queries' key"
    assert "search_results" in result_state, "State should contain the 'search_results' key"

    # Ensure the mock was called with each query
    assert mock_search_google.call_count == 3, "Expected _search_google to be called for each query"
