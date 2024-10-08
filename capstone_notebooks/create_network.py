import spacy
import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph
import json

# Load trained spacy model
output_dir = "../spacy_models/model_1/model-best"
nlp = spacy.load(output_dir)

# Load medical articles to analyze
abstracts_df = pd.read_csv('../medical_text_to_analyze.csv')

# Instantiate networkX Graph
G = nx.Graph()

# Define function for either adding or returning an existing node
def add_or_get_node(label, text):
    for node in G.nodes(data=True):
        if node[1].get('label') == label and node[1].get('text') == text:
            return node[0]
    node_id = len(G.nodes)
    G.add_node(node_id, label=label, text=text)
    return node_id

# Iterate through medical texts
for idx, row in abstracts_df.iterrows():

    # Create nodes for abstracts
    abstract_title = row['title']
    abstract_text = row['abstract']
    abstract_node_id = add_or_get_node('Abstract', abstract_text)
    G.nodes[abstract_node_id]['title'] = abstract_title
    G.nodes[abstract_node_id]['text'] = abstract_text

    # spaCy model does its thing
    doc = nlp(abstract_text)

    # Create or match nodes based on identified entities
    for ent in doc.ents:
        ent_label = ent.label_.lower()
        ent_text = ent.text
        entity_node_id = add_or_get_node(ent_label, ent_text)

        # Create relationship between abstract and entity
        G.add_edge(abstract_node_id, entity_node_id, relationship='RELATED_TO')


# Store networkX graph as json for use with 3JS
with open('capstone_network.json', 'w') as graph_json:
    json.dump(json_graph.node_link_data(G), graph_json)