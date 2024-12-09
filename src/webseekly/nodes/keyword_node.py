from src.webseekly.core.node import Node

class KeywordNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str], 
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        topics = state.get(self.input_key[0])

        if not topics:
            raise ValueError(f"State does not contain the required input key: {self.input_key[0]}")     # TODO: topicを指定しない場合の挙動
        
        keywords = []
        for topic in topics:
            keywords.append([
                f"{topic}の技術",
                f"最新の{topic}",
                f"{topic}のトレンド"
            ])

        state[self.output_key[0]] = keywords
        return state