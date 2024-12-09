from src.webseekly.core.node import Node


class VerificationNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # 例: ["scraped_data"]
        output_key: list[str],  # 例: ["verified_data"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        """
        Verifies the data in the state.

        Args:
            state (dict): The input state with data to verify.

        Returns:
            dict: The updated state with verified data.
        """
        # 入力データを取得
        scraped_data = state.get(self.input_key[0], [])
        if not isinstance(scraped_data, list):
            raise ValueError(f"Invalid data format for {self.input_key[0]}: Expected list, got {type(scraped_data)}")

        verified_data = []

        # 検証ロジック (例: データの簡単な形式チェック)
        for item in scraped_data:
            if isinstance(item, dict) and "title" in item and "links" in item:
                # 必須フィールドが揃っている場合は追加
                verified_data.append(item)
            else:
                print(f"Invalid data detected and skipped: {item}")

        # 状態を更新
        state[self.output_key[0]] = verified_data
        return state
