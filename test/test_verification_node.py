from src.webseekly.nodes.verification_node import VerificationNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    scraped_data: list[dict]
    verified_data: list[dict]


def test_verification_node():
    """
    Test the VerificationNode functionality with a single topic.
    """
    # Define input and output keys
    input_key = ["scraped_data"]
    output_key = ["verified_data"]

    # Initialize VerificationNode
    verification_node = VerificationNode(input_key, output_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("verificationnode", verification_node)
    graph_builder.set_entry_point("verificationnode")
    graph_builder.set_finish_point("verificationnode")
    graph = graph_builder.compile()

    # Define initial state
    state = {
        "scraped_data": [
            {"title": "Valid Page 1", "links": ["https://example.com/1", "https://example.com/2"]},
            {"title": "Valid Page 2", "links": ["https://example.com/3"]},
            {"invalid_key": "Invalid Data"}
        ],
        "verified_data": []
    }

    # Invoke the graph
    result_state = graph.invoke(state, debug=True)

    # Expected verified data
    expected_verified_data = [
        {"title": "Valid Page 1", "links": ["https://example.com/1", "https://example.com/2"]},
        {"title": "Valid Page 2", "links": ["https://example.com/3"]}
    ]

    # Assertions
    assert "verified_data" in result_state, "State should contain 'verified_data' key"
    assert len(result_state["verified_data"]) == len(expected_verified_data), "Number of verified items should match"
    assert result_state["verified_data"] == expected_verified_data, "Verified data does not match expected output"
