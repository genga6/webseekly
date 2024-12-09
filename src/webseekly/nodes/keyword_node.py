from src.webseekly.core.node import Node


class KeywordNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["topic"]
        output_key: list[str],  # ["keywords"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        # Retrieve the topic from the state
        topic = state.get(self.input_key[0])

        if not topic:
            raise ValueError(f"State does not contain the required input key: {self.input_key[0]}")

        # Generate keywords for the single topic
        keywords = [
            f"{topic}の技術",
            f"最新の{topic}",
            f"{topic}のトレンド"
        ]

        # Update the state with the generated keywords
        state[self.output_key[0]] = keywords
        return state
