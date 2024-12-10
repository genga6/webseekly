import os
import json
from src.webseekly.core.node import Node


class SaveNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["verified_data"]
        output_key: list[str],  # ["save_status"]
        save_path: str = "./output_data",   # Default save path for local storage
        use_cloud: bool = False, 
        cloud_client = None, 
        bucket_name = "default_bucket"
    ):
        super().__init__(input_key, output_key)
        self.save_path = save_path
        self.use_cloud = use_cloud
        self.cloud_client = cloud_client
        self.bucket_name = bucket_name

    def _save_to_local(self, data: dict, file_name: str):
        """
        Save data to the local directory.
        """
        file_path = os.path.join(self.save_path, file_name)
        try:
            os.makedirs(self.save_path, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return file_path
        
        except Exception as e:
            raise IOError(f"Failed to save file locally: {e}")
    
    def _save_to_cloud(self, data: dict, file_name: str):
        """
        Save data to the cloud storage.
        """
        if not self.cloud_client:
            raise ValueError("Cloud client is not configured.")
        try: 
            cloud_path = f"{self.save_path}/{file_name}"
            self.cloud_client.put_object(
                Bucket=self.bucket_name, 
                Key=cloud_path, 
                Body=json.dumps(data, ensure_ascii=False).encode("utf-8")
            )
            return f"s3://{self.bucket_name}/{cloud_path}"
        
        except Exception as e:
            raise IOError(f"Failed to save file to cloud: {e}")

    def execute(self, state) -> dict:
        """
        Saves the verified data to a specified directory in JSON format.

        Args:
            state (dict): The input state with data to save.

        Returns:
            dict: The updated state with save status.
        """

        verified_data = state.get(self.input_key[0], [])
        if not isinstance(verified_data, list):
            raise ValueError(f"Invalid data format for {self.input_key[0]}: Expected list, got {type(verified_data)}")

        save_status = []

        # Itarate over verified data and save each entry
        for idx, item in enumerate(verified_data):
            file_name = f"verified_data_{idx + 1}.json"
            try:
                if self.use_cloud:
                    file_path = self._save_to_cloud(item, file_name)
                else:
                    file_path = self._save_to_local(item, file_name)
                save_status.append({"file": file_path, "status": "success"})

            except Exception as e:
                print(f"Failed to save data {item}: {e}")
                save_status.append({"file": file_name, "status": f"failed: {e}"})

        state[self.output_key[0]] = save_status
        return state