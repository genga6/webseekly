from src.webseekly.nodes.keyword_node import KeywordNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    topic: str
    keywords: list[str]


def test_keyword_node():
    # Define input and output keys
    input_key = ["topic"]
    output_key = ["keywords"]

    # Create KeywordNode
    keyword_node = KeywordNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("keywordnode", keyword_node)
    graph_builder.set_entry_point("keywordnode")
    graph_builder.set_finish_point("keywordnode")
    graph = graph_builder.compile()

    # Define initial state for a single topic
    state = {
        "topic": "AI",  # Single topic
        "keywords": [],
    }

    result_state = graph.invoke(state, debug=True)

    # Assertions
    expected_keywords = ["AIの技術", "最新のAI", "AIのトレンド"]

    # Execute the graph
    assert result_state["keywords"] == expected_keywords, "Generated keywords do not match expected output"
    assert "topic" in result_state, "State should retain the 'topic' key"
    assert "keywords" in result_state, "State should contain the 'keywords' key"
