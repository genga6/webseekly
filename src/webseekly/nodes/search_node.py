from webseekly.core.node import Node


class SearchNode(Node):
    def __init__(
        self, 
        input_key: list[str], 
        output_key: list[str], 
    ):
        super().__init__(input_key, output_key)

    def execute(self, state) -> dict:
        # 'keywords' から検索を実行し、リンクを取得
        grouped_keywords = state.get(self.input_key[0])
        
        if not isinstance(grouped_keywords, list) or not all(isinstance(keywords, list) for keywords in grouped_keywords):
            raise ValueError(f"Input '{self.input_key[0]}' must be a list of lists, but got {type(grouped_keywords).__name__}")
        
        search_results = []

        for keyword_list in grouped_keywords:
            # NOTE: 実際の検索APIの利用は後回し
            topic_results = [
                f"https://example.com/search?q={keyword}" for keyword in keyword_list
            ] 
            search_results.append(topic_results)

        state[self.output_key[0]] = search_results
        return state