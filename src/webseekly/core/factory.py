from webseekly.core.node import Node
from webseekly.nodes.crawl_node import CrawlNode

class NodeFactory:
    @staticmethod
    def create_node(node_name: str, **kwargs) -> Node:
        """
        Factory method for dynamically generating nodes
        :param node_name: Node name
        :param kwargs: Additional arguments when creating a node
        :return: Node instance
        """
        # LLMnode
        if node_name == "crawl_node":
            return CrawlNode(**kwargs)

        else:
            raise ValueError(f"Unknown node type: {node_name}")