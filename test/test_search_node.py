from webseekly.nodes.search_node import SearchNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    keywords: list[list]
    search_results: list[list]


def test_search_node():
    """
    Test the SearchNode functionality.
    """
    # Define input and output keys
    input_key = ["keywords"]
    output_key = ["search_results"]

    # Initialize SearchNode
   # Create KeywordNode
    search_node = SearchNode(input_key, output_key)
    
    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("searchnode", search_node)
    graph_builder.set_entry_point("searchnode")
    graph_builder.set_finish_point("searchnode")
    graph = graph_builder.compile()

    # Define initial state
    state = {
        "keywords": [
            ["AIの技術", "最新のAI", "AIのトレンド"],
            ["Quantumの技術", "最新のQuantum", "Quantumのトレンド"]
        ],
        "search_results": [],
    }

    result_state = graph.invoke(state, debug=True)

    # Assertions
    expected_results = [
        [
            "https://example.com/search?q=AIの技術",
            "https://example.com/search?q=最新のAI",
            "https://example.com/search?q=AIのトレンド"
        ],
        [
            "https://example.com/search?q=Quantumの技術",
            "https://example.com/search?q=最新のQuantum",
            "https://example.com/search?q=Quantumのトレンド"
        ]
    ]

    # Assertions
    assert result_state["search_results"] == expected_results, "Search results do not match expected output"
    assert "keywords" in result_state, "State should retain the 'keywords' key"
    assert "search_results" in result_state, "State should contain the 'search_results' key"