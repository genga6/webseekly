from webseekly.nodes.search_node import SearchNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    keywords: list[str]
    search_results: list[str]


def test_search_node():
    """
    Test the SearchNode functionality with a single topic.
    """
    # Define input and output keys
    input_key = ["keywords"]
    output_key = ["search_results"]

    # Initialize SearchNode
    search_node = SearchNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("searchnode", search_node)
    graph_builder.set_entry_point("searchnode")
    graph_builder.set_finish_point("searchnode")
    graph = graph_builder.compile()

    # Define initial state for a single topic
    state = {
        "keywords": ["AIの技術", "最新のAI", "AIのトレンド"],  # Single topic's keywords
        "search_results": [],
    }

    result_state = graph.invoke(state, debug=True)

    # Expected search results for the single topic
    expected_results = [
        "https://example.com/search?q=AIの技術",
        "https://example.com/search?q=最新のAI",
        "https://example.com/search?q=AIのトレンド"
    ]

    # Assertions
    assert result_state["search_results"] == expected_results, "Search results do not match expected output"
    assert "keywords" in result_state, "State should retain the 'keywords' key"
    assert "search_results" in result_state, "State should contain the 'search_results' key"
