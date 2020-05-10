import collections

import matplotlib.pyplot as plt
import networkx as nx

class FlowEdge:

    def __init__(self, from_, to, capacity, flow):
        self.from_ = from_
        self.to = to
        self.capacity = capacity
        self.flow = flow

    def __repr__(self):
        return f'<{self.from_.id} → {self.to.id}>'

class Node:
    def __init__(self, id, graph):
        self.id = id
        self.edges = []
        self.backward_edges = []
        self.graph = graph
        self.visited = False

    def edge_to(self, id, capacity, flow):
        edge = FlowEdge(self, self.graph[id], capacity, flow)
        self.edges.append(edge)
        self.graph[id].backward_edges.append(edge)

    def max_flow_edmonds_karp(self, sink):
        found_augmenting_path = True
        while found_augmenting_path:
            for n in self.graph:
                n.visited = False
            found_augmenting_path = self.augmenting_path_bfs(sink)

        return sum(bw_edge.flow for bw_edge in sink.backward_edges)

    def augmenting_path_bfs(self, sink):
        queue = collections.deque([(self, [], [], float('inf'))])
        self.visited = True
        while queue:
            last_node, path, change_dirs, max_flow_change = queue.popleft()
            if last_node is sink:
                for edge, change_dir in zip(path, change_dirs):
                    edge.flow += change_dir * max_flow_change
                return True
            else:
                for edge in last_node.edges:
                    if edge.flow < edge.capacity and not edge.to.visited:
                        edge.to.visited = True
                        queue.append((edge.to, path + [edge], change_dirs + [1], min(max_flow_change, edge.capacity-edge.flow)))
                for bw_edge in last_node.backward_edges:
                    if bw_edge.flow > 0 and not bw_edge.from_.visited:
                        bw_edge.from_.visited = True
                        queue.append((bw_edge.from_, path + [bw_edge], change_dirs + [-1], min(max_flow_change, bw_edge.flow)))
        return False

    def max_flow_ford_fulkerson(self, sink):
        found_augmenting_path = True
        while found_augmenting_path:
            for n in self.graph:
                n.visited = False
            found_augmenting_path = self.augmenting_path_dfs(sink, [], [], float('inf'))

        return sum(bw_edge.flow for bw_edge in sink.backward_edges)

    def augmenting_path_dfs(self, sink, path, flow_change_dirs, max_flow_change):
        if self is sink:
            #print([(e.from_.id, e.to.id) for e in path])
            for edge, change_dir in zip(path, flow_change_dirs):
                edge.flow += change_dir * max_flow_change
            return True

        self.visited = True
        for edge in self.edges:
            if edge.flow < edge.capacity and not edge.to.visited:
                found_path = edge.to.augmenting_path_dfs(sink, path + [edge], flow_change_dirs + [1],
                                                         min(max_flow_change, edge.capacity-edge.flow))
                if found_path:
                    return True
        for bw_edge in self.backward_edges:
            if bw_edge.flow > 0 and not bw_edge.from_.visited:
                found_path = bw_edge.from_.augmenting_path_dfs(sink, path + [bw_edge], flow_change_dirs + [-1],
                                                         min(max_flow_change, bw_edge.flow))
                if found_path:
                    return True
        return False

    def __repr__(self):
        return '[' + str(self.id) + ']: ' + ", ".join(["(→ " + str(edge.to.id) + f': c={edge.capacity} f={edge.flow}' + ")" for edge in self.edges])


def print_graph(graph):
    print('\n'.join(map(str, graph)))

def create_graph(n):
    graph = []
    for i in range(n):
        graph.append(Node(i, graph))
    return graph, graph[0], graph[-1]

def graph_to_networkx(graph):
    G = nx.DiGraph()
    G.add_nodes_from(range(len(graph)))
    for node in graph:
        for edge in node.edges:
            G.add_edge(edge.from_.id, edge.to.id, capacity=edge.capacity, flow=edge.flow)
    return G

def draw_graph(graph, omit_labels=False):
    G = graph_to_networkx(graph)
    layout = nx.drawing.nx_pydot.graphviz_layout(G)
    nx.draw_networkx(G, pos=layout)
    if not omit_labels:
        edge_labels = nx.draw_networkx_edge_labels(G, pos=layout)
    plt.show()

