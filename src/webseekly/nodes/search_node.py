from webseekly.core.node import Node


class SearchNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["keywords"]
        output_key: list[str],  # ["search_results"]
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        """
        Executes the search operation for a single topic.
        Generates search result URLs based on the provided keywords.
        """
        keywords = state.get(self.input_key[0])

        if not isinstance(keywords, list) or not all(isinstance(keyword, str) for keyword in keywords):
            raise ValueError(f"Input '{self.input_key[0]}' must be a list of strings, but got {type(keywords).__name__}")

        # Generate search result URLs
        search_results = [
            f"https://example.com/search?q={keyword}" for keyword in keywords
        ]

        # Update state with the search results
        state[self.output_key[0]] = search_results
        return state
