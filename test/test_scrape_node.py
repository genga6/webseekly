import os
import json
import pytest
from unittest.mock import patch, MagicMock
from src.webseekly.nodes.scrape_node import ScrapeNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    crawled_data: dict  # Example: {"content": "<html><title>Test</title><body>Sample Content</body></html>"}
    search_intent: str  # Example: "Extract the title and body content from the web page"
    required_fields: list[str]  # Example: ["title", "body"]
    scraped_data: dict  # Example: {"title": "Test", "body": "Sample Content"} 


def test_scrape_node():
    input_key = ["crawled_data", "search_intent", "required_fields"]
    output_key = ["scraped_data"]

    openai_api_key = os.getenv("OPEN_API_KEY")

    scrape_node = ScrapeNode(input_key, output_key, openai_api_key=openai_api_key)

    # モックデータを作成
    crawled_data = {
        "content": "<html><title>Test Title</title><meta name='description' content='This is a meta description.'><body>Sample Content</body></html>"
    }
    search_intent = "Extract the title and body content from the web page"
    required_fields = ["title", "body"]

    state = {
        "crawled_data": crawled_data,
        "search_intent": search_intent,
        "required_fields": required_fields,
        "scraped_data": {}
    }

    # LLMの応答をモック
    mock_llm_response = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({"title": "Test Title", "body": "Sample Content"})
                }
            }
        ]
    }

    # BeautifulSoup + LLMの動作をパッチ
    with patch("openai.ChatCompletion.create", return_value=mock_llm_response) as mock_openai:
        # StateGraphを作成
        graph_builder = StateGraph(State)
        graph_builder.add_node("scrapenode", scrape_node)
        graph_builder.set_entry_point("scrapenode")
        graph_builder.set_finish_point("scrapenode")
        graph = graph_builder.compile()

        # 実行
        result_state = graph.invoke(state, debug=True)

        # 期待される結果
        expected_scraped_data = {
            "title": "Test Title",
            "body": "Sample Content",
            "other_fields": None,
            "error_message": None
        }

        # アサーション
        assert result_state["scraped_data"]["title"] == expected_scraped_data["title"], "タイトルが一致しません"
        assert result_state["scraped_data"]["body"] == expected_scraped_data["body"], "本文が一致しません"
        assert result_state["scraped_data"]["error_message"] is None, "予期しないエラーメッセージが含まれています"

    # モックが正しく呼び出されたことを確認
    mock_openai.assert_called_once()