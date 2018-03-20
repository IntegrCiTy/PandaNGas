from pandangas.edit import EditNetwork


class Network:
    def __init__(self):
        self.edit = EditNetwork()

    @property
    def nodes(self):
        return self.edit.nodes

    @property
    def pipes(self):
        return self.edit.pipes
