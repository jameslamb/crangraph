from flask import Flask, render_template, jsonify
import networkx as nx
from networkx.readwrite import json_graph

app = Flask(__name__)
 
def getGraph():
	G = nx.read_edgelist('scratch_space/test_edge_list.txt', nodetype=str, create_using=nx.DiGraph())
	for n in G: # so that d3 picks up on this!
		G.node[n]['name'] = n
	return G

def get_subgraph(package="ggplot", path_length=2):
    package_list = set([package])
    neighbors = G.neighbors(package)
    package_list.update(neighbors)
    if path_length == 2:
        for neighbor in neighbors:
            neighbor_2 = G.neighbors(neighbor)
            package_list.update(neighbor_2)
    return G.subgraph(package_list)


G = getGraph()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data/")
@app.route("/data/<package>")
def data(package="ggplot"):
	return jsonify(json_graph.node_link_data(get_subgraph(package)))


if __name__ == "__main__":
    app.run()
