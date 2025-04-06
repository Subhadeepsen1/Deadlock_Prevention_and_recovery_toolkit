import networkx as nx
import matplotlib.pyplot as plt

def show_resource_allocation_graph(self):
    G = nx.DiGraph()
    allocation_edges = []
    request_edges = []

    for i in range(self.processes):
        G.add_node(f"P{i}", color='blue')
    for j in range(self.resources):
        G.add_node(f"R{j}", color='red')

    for i in range(self.processes):
        for j in range(self.resources):
            allocated = int(self.matrix_table.item(i * 3, j + 1).text())
            requested = int(self.matrix_table.item(i * 3 + 2, j + 1).text())

            if allocated > 0:
                allocation_edges.append((f"R{j}", f"P{i}"))
            if requested > 0:
                request_edges.append((f"P{i}", f"R{j}"))

    print("Allocation Edges:", allocation_edges)
    print("Request Edges:", request_edges)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True,
            node_color=['blue' if node.startswith('P') else 'red' for node in G.nodes()])
    nx.draw_networkx_edges(G, pos, edgelist=allocation_edges, edge_color="green", arrowstyle="->", width=2)
    nx.draw_networkx_edges(G, pos, edgelist=request_edges, edge_color="orange", arrowstyle="->", width=2, style="dashed")
    plt.title("Resource Allocation Graph\n(Green: Allocated, Orange: Requested)")
    plt.show()
