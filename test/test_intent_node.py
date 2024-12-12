import os
from unittest.mock import patch
from webseekly.nodes.intent_node import IntentNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    user_input: str
    search_intent: str
    queries: list[str]
    error_message: str


def test_intent_node():
    # Define input and output keys
    input_key = ["user_input"]
    output_key = ["search_intent", "queries"]

    openai_api_key = os.getenv("OPEN_API_KEY")

    # Create IntentNode
    intent_node = IntentNode(input_key, output_key, openai_api_key=openai_api_key)

    # Build the state graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("intentnode", intent_node)
    graph_builder.set_entry_point("intentnode")
    graph_builder.set_finish_point("intentnode")
    graph = graph_builder.compile()

    # Define initial state for a single topic
    state = {
        "user_input": "AI技術の最新トレンドについて知りたい",
        "search_intent": "",
        "queries": [],
        "error_message": ""
    }

    # Mock OpenAI API response
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": '{"search_intent": "AI技術の最新トレンドを調査", "queries": ["最新AI技術", "AIトレンド 2024"]}'
                }
            }
        ]
    }

    with patch("openai.ChatCompletion.create", return_value=mock_response) as mock_openai:
        # Execute the graph
        result_state = graph.invoke(state, debug=True)

        # Assertions
        assert result_state["search_intent"] == "AI技術の最新トレンドを調査", "Search intent does not match expected value"
        assert "最新AI技術" in result_state["queries"], "Keyword '最新AI技術' is missing in queries"
        assert "AIトレンド 2024" in result_state["queries"], "Keyword 'AIトレンド 2024' is missing in queries"
        assert "error_message" not in result_state or result_state["error_message"] == "", "Unexpected error_message present"

        # Ensure the mock was called as expected
        mock_openai.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはユーザーの検索意図を理解し、適切なキーワードを生成するアシスタントです。"},
                {"role": "user", "content": (
                    "以下のユーザー入力を基に、検索意図(search_intent)と関連するキーワード(queries)を生成してください。\n"
                    "1. 検索意図はユーザーが何を知りたいかを簡潔に表現した内容としてください。\n"
                    "2. キーワードは具体的なフレーズや単語をリスト形式で作成してください。\n\n"
                    "ユーザー入力: AI技術の最新トレンドについて知りたい\n\n"
                    "出力形式:\n"
                    "{\n    \"search_intent\": \"...\",\n    \"queries\": [\"...\", \"...\"]\n}"
                )}
            ],
            max_tokens=100,
            temperature=0.7
        )