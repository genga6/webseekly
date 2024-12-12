import openai
import json
from bs4 import BeautifulSoup
from src.webseekly.core.node import Node
from typing import TypedDict, Any


class ScrapedData(TypedDict, total=False):
    title: str
    body: str
    other_fields: dict[str, Any] | None
    error_message: str | None


class ScrapeNode(Node):
    def __init__(
        self,
        input_key: list[str],  # e.g., ["crawled_data", "search_intent", "required_fields"]
        output_key: list[str],  # e.g., ["scraped_data"]
        openai_api_key: str
    ):
        super().__init__(input_key, output_key)
        openai.api_key = openai_api_key

    def _extract_with_bs4(self, content: str) -> dict:
        """
        Extracts basic information from HTML using BeautifulSoup.
        """
        
        soup = BeautifulSoup(content, "html.parser")
        extracted_data = {
            "title": soup.title.string if soup.title else None,
            "meta_description": soup.find("meta", {"name": "description"})["content"]
            if soup.find("meta", {"name": "description"}) else None,
            "text": soup.get_text()
        }
        return extracted_data

    def _map_fields_with_llm(self, extracted_data: dict, search_intent: str, required_fields: list[str]) -> dict:
        """
        Maps required fields to extracted data using LLM.
        """
        try:
            prompt = (
                f"""
                以下の抽出データ(extracted_data)と検索意図(search_intent)を基に、各フィールド(required_fields)に適合するデータを特定してください。
                extracted_data: {extracted_data}
                search_intent: {search_intent}
                required_fields: {required_fields}
                                

                出力形式:
                {{
                    "field_name": "extracted_value",
                    ...
                }}
                """
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたはデータマッピングアシスタントです。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            mapped_data = json.loads(response['choices'][0]['message']['content'])
            return mapped_data
        except Exception as e:
            return {field: None for field in required_fields}

    def execute(self, state: dict) -> dict:
        """
        Extracts and maps data from crawled_data based on required_fields and search_intent.
        """
        # Retrieve inputs
        crawled_data = state.get(self.input_key[0], "")
        search_intent = state.get(self.input_key[1], {})
        required_fields = state.get(self.input_key[2], [])

        # Handle missing inputs
        if not required_fields or not crawled_data:
            state[self.output_key[0]] = ScrapedData(
                title=None,
                body=None,
                other_fields=None,
                error_message="required_filedまたはcrawled_dataが不足しています。"
            )
            return state

        # Extract basic information using BeautifulSoup
        extracted_data = self._extract_with_bs4(crawled_data["content"])

        # Map fields to the extracted data using LLM
        mapped_data = self._map_fields_with_llm(extracted_data, search_intent, required_fields)

        # Update state with the output
        state[self.output_key[0]] = ScrapedData(
            title=mapped_data.get("title"),
            body=mapped_data.get("body"),
            other_fields={key: value for key, value in mapped_data.items() if key not in ["title", "body"]},
            error_message=None if all(mapped_data.values()) else "一部のフィールドに適合するデータが見つかりませんでした。"
        )

        return state