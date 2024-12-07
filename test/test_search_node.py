from webseekly.nodes.search_node import SearchNode

def test_search_node():
    search_node = SearchNode()
    initial_state = {
        "keywords": ["AIの技術", "最新のAI", "AIのトレンド"]
    }
    updated_state = search_node(initial_state)
    print("Updated State:", updated_state)