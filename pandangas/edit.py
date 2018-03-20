import pandas as pd


class EditNetwork:
    """
    Class gathering network edition methods
    """
    def __init__(self):
        self.nodes = pd.DataFrame(columns=["type", "x", "y", "level"])
        self.pipes = pd.DataFrame(columns=["diameter", "length", "node_a", "node_b"])

    def add_node(self, node, x, y, level, node_type="NODE"):
        assert level in ["BP", "MP"]
        assert node_type in ["NODE", "FEEDER", "SINK", "SUB_MP", "SUB_BP"]
        self.nodes.loc[node] = [node_type, x, y, level]
        return node

    def add_pipe(self, node_a, node_b, length, diameter):
        if {node_a, node_b}.issubset(set(self.nodes.index)):
            pipe = "P_{}_{}".format(node_a, node_b)
            self.pipes.loc[pipe] = [diameter, length, node_a, node_b]
            return pipe

    def add_feeder(self, node, x, y):
        return self.add_node(node, x, y, "MP", node_type="FEEDER")

    def add_consumer(self, node, x, y, level):
        self.add_node(node, x, y, level, node_type="SINK")

    def add_station(self, node, x, y):
        node_mp = self.add_node(node+"_MP", x, y, "MP", node_type="SUB_MP")
        node_bp = self.add_node(node+"_BP", x, y, "BP", node_type="SUB_BP")
        return node_mp, node_bp
