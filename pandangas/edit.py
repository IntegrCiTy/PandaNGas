import pandas as pd
import networkx as nx


class EditNetwork:
    """
    Class gathering network edition methods
    """
    def __init__(self):
        self.nodes = pd.Dataframe()
        self.pipes = pd.Dataframe()
        self.graph = nx.DiGraph()

    def add_node(self, node, node_type="NODE"):
        return node

    def add_pipe(self):
        pass

    def add_feeder(self, node):
        self.add_node(node_type="FEEDER")

    def add_consumer(self, node):
        self.add_node(node_type="SINK")

    def add_station(self, node):
        node_mp = self.add_node(node_type="SUB_MP")
        node_bp = self.add_node(node_type="SUB_BP")
