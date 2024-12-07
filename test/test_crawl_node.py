from langgraph.nodes.crawl_node import CrawlNode

def test_crawl_node():
    crawl_node = CrawlNode()
    initial_state = {
        "search_results": [
            "https://example.com/search?q=AIの技術",
            "https://example.com/search?q=最新のAI"
        ]
    }
    updated_state = crawl_node(initial_state)
    print("Updated State:", updated_state)