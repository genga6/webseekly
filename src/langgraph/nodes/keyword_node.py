from typing import TypedDict

class State(TypedDict):
    topic: str
    keywords: list[str]

class KeywordNode:
    def __init__(self):
        pass

    def __call__(self, state: State) -> dict:
        topic = state.get("topic")
        if topic:
            keywords = [f"{topic}の技術", f"最新の{topic}", f"{topic}のトレンド"]   # TODO: APIによる機能強化
            state["keywords"] = keywords
        else:
            state["keywords"] = []

        return state
    
if __name__ == "__main__":
    keyword_node = KeywordNode()
    initial_state = {"topic": "AI"}
    updated_state = keyword_node(initial_state)
    print("Updated State:", updated_state)