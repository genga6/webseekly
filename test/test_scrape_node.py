import pytest
from unittest.mock import patch, Mock
from src.webseekly.nodes.scrape_node import ScrapeNode
from langgraph.graph import StateGraph
from typing import TypedDict


class State(TypedDict):
    crawled_data: list[list[str]]  # トピックごとにURLをリスト化
    scraped_data: list[list[dict]]  # トピックごとのスクレイピング結果


@pytest.fixture
def mock_playwright_browser():
    with patch("src.webseekly.nodes.scrape_node.sync_playwright") as mock_playwright:
        mock_browser = Mock()
        mock_page = Mock()
        mock_context = Mock()

        mock_playwright.return_value.__enter__.return_value = Mock(
            chromium=Mock(
                launch=Mock(return_value=mock_browser)
            )
        )
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # モックの設定
        mock_page.content.return_value = "<html><head><title>Mocked Page</title></head><body><a href='https://mocklink1.com'>Link1</a><a href='https://mocklink2.com'>Link2</a></body></html>"
        mock_page.title.return_value = "Mocked Page"
        mock_page.query_selector_all.return_value = [
            Mock(get_attribute=Mock(return_value="https://mocklink1.com")),
            Mock(get_attribute=Mock(return_value="https://mocklink2.com")),
        ]

        yield mock_playwright


def test_scrape_node(mock_playwright_browser):
    input_key = ["crawled_data"]
    output_key = ["scraped_data"]

    scrape_node = ScrapeNode(input_key, output_key)

    # トピックごとにURLを分けた状態を初期データとして設定
    state = {
        "crawled_data": [
            ["https://example.com/page1", "https://example.com/page2"],  # トピック1
            ["https://example.com/page3"]  # トピック2
        ],
        "scraped_data": []
    }

    graph_builder = StateGraph(State)
    graph_builder.add_node("scrapenode", scrape_node)
    graph_builder.set_entry_point("scrapenode")
    graph_builder.set_finish_point("scrapenode")
    graph = graph_builder.compile()

    # 実行
    result_state = graph.invoke(state, debug=True)

    # 期待される結果を設定
    expected_scraped_data = [
        [  # トピック1
            {"title": "Mocked Page", "links": ["https://mocklink1.com", "https://mocklink2.com"]},
            {"title": "Mocked Page", "links": ["https://mocklink1.com", "https://mocklink2.com"]}
        ],
        [  # トピック2
            {"title": "Mocked Page", "links": ["https://mocklink1.com", "https://mocklink2.com"]}
        ]
    ]

    # アサーション
    assert "scraped_data" in result_state, "State should contain 'scraped_data' key"
    assert len(result_state["scraped_data"]) == len(expected_scraped_data), "Number of topics should match"
    assert result_state["scraped_data"] == expected_scraped_data, "Scraped data does not match expected content"
