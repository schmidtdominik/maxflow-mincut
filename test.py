from graph import *
import networkx as nx

graph, source, sink = create_graph(4)
graph[0].edge_to(1, 5, 0)
graph[0].edge_to(2, 3, 0)
graph[1].edge_to(3, 1, 0)
graph[1].edge_to(2, 4, 0)
graph[2].edge_to(3, 4, 0)

value_ff = source.max_flow_ford_fulkerson(sink)
value_ek = source.max_flow_edmonds_karp(sink)
print(value_ff, value_ek)
draw_graph(graph)

