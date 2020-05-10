import random
from graph import *
import networkx as nx

def get_random_graph(seed):
    random.seed(seed)
    node_count = 30
    graph, source, sink = create_graph(node_count)
    edges = {(random.randint(0, node_count - 1), random.randint(0, node_count - 1)) for i in range(100)}
    for a, b in edges:
        if a != b:
            graph[a].edge_to(b, random.randint(1, 200), 0)
    return graph, source, sink

def reset_flow(graph):
    for n in graph:
        n.flow = 0

seed = random.randint(0, 99999999)
graph, source, sink = get_random_graph(seed)

value = nx.maximum_flow_value(graph_to_networkx(graph), source.id, sink.id)

reset_flow(graph)
value1 = source.max_flow_edmonds_karp(sink)

reset_flow(graph)
value2 = source.max_flow_ford_fulkerson(sink)

print(value, value1, value2)
print_graph(graph)
draw_graph(graph, omit_labels=True)