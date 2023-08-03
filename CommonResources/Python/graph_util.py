class Graph:
    def __init__(self, *nodes):
        self.nodes = nodes

    def __repr__(self):
        return f"Graph{self.nodes}"
