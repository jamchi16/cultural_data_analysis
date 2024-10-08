import json
import networkx as nx
from networkx.readwrite import json_graph

# Load the JSON graph
with open('../3D-Graph/capstone_network.json', 'r') as graph_json:
    graph_data = json.load(graph_json)
    G = json_graph.node_link_graph(graph_data)



# Compute the best partition
communities = nx.community.louvain_communities(G, seed=123)
for index, community in enumerate(communities):
    for nodeid in community:
        G.nodes[nodeid]['community'] = index


# Compute degree centrality
degree_centrality = nx.degree_centrality(G)

# Assign degree centrality values to nodes
for node_id, centrality in degree_centrality.items():
    G.nodes[node_id]['degree_centrality'] = centrality

# Store networkX graph as json for use with 3JS
with open('capstone_gds_network.json', 'w') as graph_json:
    json.dump(json_graph.node_link_data(G), graph_json)