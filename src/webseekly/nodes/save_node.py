import os
import json
from src.webseekly.core.node import Node


class SaveNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # 例: ["verified_data"]
        output_key: list[str],  # 例: ["save_status"]
        save_path: str = "./output_data"  # 保存先ディレクトリ（デフォルトはローカルのoutput_dataフォルダ）
    ):
        super().__init__(input_key, output_key)
        self.save_path = save_path

    def execute(self, state) -> dict:
        """
        Saves the verified data to a specified directory in JSON format.

        Args:
            state (dict): The input state with data to save.

        Returns:
            dict: The updated state with save status.
        """
        # 入力データを取得
        verified_data = state.get(self.input_key[0], [])
        if not isinstance(verified_data, list):
            raise ValueError(f"Invalid data format for {self.input_key[0]}: Expected list, got {type(verified_data)}")

        # 保存先ディレクトリの作成
        os.makedirs(self.save_path, exist_ok=True)

        save_status = []

        # データ保存
        for idx, item in enumerate(verified_data):
            file_path = os.path.join(self.save_path, f"verified_data_{idx + 1}.json")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, ensure_ascii=False, indent=4)
                save_status.append({"file": file_path, "status": "success"})
            except Exception as e:
                print(f"Failed to save data {item}: {e}")
                save_status.append({"file": file_path, "status": f"failed: {e}"})

        # 状態を更新
        state[self.output_key[0]] = save_status
        return state
