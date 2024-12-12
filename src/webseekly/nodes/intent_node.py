import os
import openai
from src.webseekly.core.node import Node
from pydantic import BaseModel
import json


class IntentNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["user_input"]
        output_key: list[str],  # ["search_intent", "queries"]
        openai_api_key: str
    ):
        super().__init__(input_key, output_key)
        openai.api_key = openai_api_key

    def _generate_intent_and_queries(self, user_input: str) -> dict:
        """
        Generates search intent and queries using OpenAI API.
        """
        try:
            prompt = (
                "以下のユーザー入力を基に、検索意図(search_intent)と関連するキーワード(queries)を生成してください。\n"
                "1. 検索意図はユーザーが何を知りたいかを簡潔に表現した内容としてください。\n"
                "2. キーワードは具体的なフレーズや単語をリスト形式で作成してください。\n\n"
                f"ユーザー入力: {user_input}\n\n"
                "出力形式:\n"
                "{\n    \"search_intent\": \"...\",\n    \"queries\": [\"...\", \"...\"]\n}"
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたはユーザーの検索意図を理解し、適切なキーワードを生成するアシスタントです。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            content = response['choices'][0]['message']['content'].strip()
            intent_data = json.loads(content)  # Convert the API response text to a dictionary
            return intent_data
        except json.JSONDecodeError as e:
            # Handle JSON decoding issues
            return {
                "search_intent": "AI関連情報の検索",
                "queries": ["AI", "人工知能"],
                "error_message": "JSONデコードエラー: 出力形式を確認してください。"
            }
        except Exception as e:
            # Handle other errors and provide default values
            return {
                "search_intent": "AI関連情報の検索",
                "queries": ["AI", "人工知能"],
                "error_message": str(e)
            }

    def execute(self, state) -> dict:
        """
        Processes user input to generate search intent and queries.
        """
        user_input = state.get(self.input_key[0], "")

        if not user_input:
            # Handle missing or empty user input
            state[self.output_key[0]] = "意図が不明です"
            state[self.output_key[1]] = []
            state["error_message"] = "ユーザー入力が空です。具体的な検索意図を入力してください。"
            return state

        # Generate intent and queries
        intent_data = self._generate_intent_and_queries(user_input)

        # Update state with the output
        state[self.output_key[0]] = intent_data.get("search_intent", "意図が不明です")
        state[self.output_key[1]] = intent_data.get("queries", [])
        if "error_message" in intent_data:
            state["error_message"] = intent_data["error_message"]

        # Provide feedback for ambiguous input
        if not state[self.output_key[1]]:
            state["error_message"] = "生成されたキーワードがありません。検索意図を具体化してください。"

        return state
