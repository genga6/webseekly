from typing import TypedDict
from webseekly.graph import StateGraph
from nodes.keyword_node import KeywordNode
from nodes.search_node import SearchNode
from nodes.crawl_node import CrawlNode
from nodes.scrape_node import ScrapeNode
from nodes.verification_node import VerificationNode
from nodes.save_node import SaveNode

class State(TypedDict):
    topic: str
    keywords: list[str]
    search_results: list[str]
    crawled_data: list[str]
    scraped_data: list[dict]
    verified_data: list[dict] | None
    saved: bool

class WebSeeklyWorkflow:
    def __init__(self):
        self.graph_builder = StateGraph(State)

        self.keyword_node = KeywordNode()
        self.search_node = SearchNode()
        self.crawl_node = CrawlNode()
        self.scrape_node = ScrapeNode()
        self.verification_node = VerificationNode()
        self.save_node = SaveNode()

        self.graph_builder.add_node("keyword_node", self.keyword_node)
        self.graph_builder.add_node("search_node", self.search_node)
        self.graph_builder.add_node("crawl_node", self.crawl_node)
        self.graph_builder.add_node("scrape_node", self.scrape_node)
        self.graph_builder.add_node("verification_node", self.verification_node)
        self.graph_builder.add_node("save_node", self.save_node)

        self.graph_builder.set_entry_point("keyword_node")
        self.graph_builder.set_finish_point("save_node")

        self.graph = self.graph_builder.compile()

    def run(self, input_data):
        state: State = {'topic': input_data}
        return self.graph.invoke(state)

if __name__ == "__main__":
    workflow = WebSeeklyWorkflow()
    result = workflow.run("テクノロジー")
    print("Workflow Result:", result)

