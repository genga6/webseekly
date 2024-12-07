from langgraph.nodes.keyword_node import KeywordNode

def test_keyword_node():
    keyword_node = KeywordNode()
    initial_state = {"topic": "AI"}
    updated_state = keyword_node(initial_state)
    print("Updated State:", updated_state)