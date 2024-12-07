from typing import TypedDict

class State(TypedDict):
    keywords: list[str]
    search_results: list[str]

class SearchNode:
    def __init__(self):
        pass

    def __call__(self, state: State) -> dict:
        # 'keywords' から検索を実行し、リンクを取得
        keywords = state.get("keywords", [])
        search_results = []

        for keyword in keywords:
            # NOTE: 実際の検索APIの利用は後回し
            search_results.append(f"https://example.com/search?q={keyword}")

        state["search_results"] = search_results
        return state
    
if __name__ == "__main__":
    search_node = SearchNode()
    initial_state = {
        "keywords": ["AIの技術", "最新のAI", "AIのトレンド"]
    }
    updated_state = search_node(initial_state)
    print("Updated State:", updated_state)