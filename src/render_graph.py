import logging, json, os
import networkx as nx
import matplotlib.pyplot as plt


def main():
    logging.basicConfig(level=logging.INFO)
    file_path = os.getenv('WIKI_FILE', 'wiki.json')
    try:
        with open(file_path, 'r') as file:
            db = json.load(file)
    except:
        raise BaseException("Database not found")
    nodes, edges = set(), []
    parsing(node=db[0], prev=None, nodes=nodes, edges=edges)
    graph(nodes, edges)


def parsing(node: dict, prev: dict=None, nodes: set = {}, edges: list = []):
    nodes.add(node['title'])
    if prev:
        edges.append((prev['title'], node['title']))
    for node2 in node["members"]:
        parsing(node2, node, nodes, edges)
            

def graph(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    incoming_edges = dict(G.degree())
    sizes = [v * 100 for v in incoming_edges.values()]
    plt.figure(figsize=(90, 90), frameon=False)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='#66459c', linewidths=None)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=30, verticalalignment='bottom', horizontalalignment='left')
    plt.savefig('wiki_graph.png')


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        logging.warning(e)