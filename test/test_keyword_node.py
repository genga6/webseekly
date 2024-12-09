from src.webseekly.nodes.keyword_node import KeywordNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    topics: list[str]
    keywords: list[list]


def test_keyword_node():
    
    # Define input and output keys
    input_key = ["topics"]
    output_key = ["keywords"]

    # Create KeywordNode
    keyword_node = KeywordNode(input_key, output_key)
    
    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("keywordnode", keyword_node)
    graph_builder.set_entry_point("keywordnode")
    graph_builder.set_finish_point("keywordnode")
    graph = graph_builder.compile()

    # Define initial state
    state = {
        "topics": ["AI", "Quantum"], 
        "keywords": [],
    }

    result_state = graph.invoke(state, debug=True)

    # Assertions
    expected_keywords = [
        ["AIの技術", "最新のAI", "AIのトレンド"],
        ["Quantumの技術", "最新のQuantum", "Quantumのトレンド"]
    ]

    # Execute the graph
    assert result_state["keywords"] == expected_keywords, "Generated keywords do not match expected output"
    assert "topics" in result_state, "State should retain the 'topics' key"
    assert "keywords" in result_state, "State should contain the 'keywords' key"