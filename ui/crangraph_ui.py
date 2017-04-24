from flask import Flask, render_template, jsonify
import networkx as nx
import psycopg2
from networkx.readwrite import json_graph

app = Flask(__name__)

# Connect to DB
conn = psycopg2.connect(database="crangraph",
                                     user="postgres",
                                     password="pass",
                                     host="localhost",
                                     port="5432")
cur = conn.cursor()
 
def getGraph(package="ggplot2"):

    # Build up a set of all dependencies
    all_dep_groups = list() # set of (pkg, [deps]) tuples

    # Hit DB to create the edge_list
    cur.execute("SELECT pkgname, depstr FROM crandeps WHERE pkgname = %s", (package,))
    main_deps = cur.fetchone()
    all_dep_groups.append(main_deps)
    conn.commit()

    # Grab all the other dependencies
    other_deps = main_deps[1]['dependencies']
    for pkg in other_deps:
        cur.execute("SELECT pkgname, depstr FROM crandeps WHERE pkgname = %s", (pkg.encode('utf-8'),))
        this_dep_group = cur.fetchone()
        if this_dep_group != None and len(this_dep_group) > 0:
            all_dep_groups.append(this_dep_group)
        conn.commit()

    # Create a graph and get it poppin
    G = nx.DiGraph()
    for dep_group in all_dep_groups:
        from_pkg = dep_group[0]

        # Add a node for this main package
        if not from_pkg in G.nodes():
            G.add_node(from_pkg)

        # Add nodes and edges for all this package's dependencies
        for dep_pkg in dep_group[1]['dependencies']:
            if not dep_pkg in G.nodes():
                G.add_node(dep_pkg)
            G.add_edge(from_pkg, dep_pkg)

    # Add name attribute so D3 picks it up
    for n in G:
        G.node[n]['name'] = n

    return G

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data/")
@app.route("/data/<package>")
def data(package="ggplot"):
    return jsonify(json_graph.node_link_data(getGraph(package)))


if __name__ == "__main__":
    app.run()
