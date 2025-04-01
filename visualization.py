import networkx as nx
import matplotlib.pyplot as plt


def visualize_allocation_graph():
    G = nx.DiGraph()

    # Example Processes and Resources
    processes = ["P0", "P1", "P2", "P3", "P4"]
    resources = ["R0", "R1", "R2"]

    # Add nodes
    for p in processes:
        G.add_node(p, shape="circle", color="lightblue")

    for r in resources:
        G.add_node(r, shape="square", color="pink")

    # Example edges (Allocation and Request)
    allocation = [("R0", "P0"), ("R1", "P1"), ("R2", "P2"), ("R0", "P3"), ("R1", "P4")]
    request = [("P1", "R2"), ("P3", "R1")]

    # Add allocation edges
    G.add_edges_from(allocation, color="green")

    # Add request edges
    G.add_edges_from(request, color="red")

    # Draw graph
    pos = nx.spring_layout(G)
    edge_colors = [G[u][v]["color"] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightgray", edge_color=edge_colors, arrows=True)

    # Highlight resource nodes
    nx.draw_networkx_nodes(G, pos, nodelist=resources, node_shape="s", node_color="lightcoral")

    plt.title
