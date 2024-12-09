import os
import pytest
from src.webseekly.nodes.save_node import SaveNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    verified_data: list[dict]
    save_status: list[dict]


@pytest.fixture
def cleanup_saved_files():
    """Clean up test-generated files after testing."""
    yield
    output_dir = "./test/output_data"
    if os.path.exists(output_dir):
        for file_name in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(output_dir)


def test_save_node(cleanup_saved_files):
    # Define input and output keys
    input_key = ["verified_data"]
    output_key = ["save_status"]
    save_path = "./test/output_data"

    # Ensure the directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Create SaveNode
    save_node = SaveNode(input_key, output_key, save_path=save_path)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("savenode", save_node)
    graph_builder.set_entry_point("savenode")
    graph_builder.set_finish_point("savenode")
    graph = graph_builder.compile()

    # Define initial state for a single topic
    state = {
        "verified_data": [
            {"title": "Valid Page 1", "links": ["https://example.com/1", "https://example.com/2"]},
            {"title": "Valid Page 2", "links": ["https://example.com/3"]}
        ],
        "save_status": []
    }

    # Execute the graph
    result_state = graph.invoke(state, debug=True)

    # Verify the expected results
    expected_files = [
        os.path.join(save_path, "verified_data_1.json"),
        os.path.join(save_path, "verified_data_2.json"),
    ]
    expected_status = [
        {"file": expected_files[0], "status": "success"},
        {"file": expected_files[1], "status": "success"}
    ]

    # Assertions
    assert "save_status" in result_state, "State should contain 'save_status' key"
    assert len(result_state["save_status"]) == len(expected_status), "Number of saved files should match"
    assert result_state["save_status"] == expected_status, "Saved file status does not match expected output"

    # Check if files are actually saved
    for file_path in expected_files:
        assert os.path.exists(file_path), f"File {file_path} should exist"
