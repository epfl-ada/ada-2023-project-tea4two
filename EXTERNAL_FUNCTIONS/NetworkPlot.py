import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import numpy as np
import plotly.graph_objects as go

# Helper function for printing various graph properties
def describe_graph(G):
    print(G)
    if nx.is_connected(G):
        print("Avg. Shortest Path Length: %.4f" %nx.average_shortest_path_length(G))
        print("Diameter: %.4f" %nx.diameter(G)) # Longest shortest path
    else:
        print("Graph is not connected")
        print("Diameter and Avg shortest path length are not defined!")
    print("Sparsity: %.4f" %nx.density(G))  # #edges/#edges-complete-graph
    # #closed-triplets(3*#triangles)/#all-triplets
    print("Global clustering coefficient aka Transitivity: %.4f" %nx.transitivity(G))

# Helper function for visualizing the graph
def visualize_graph(G, with_labels=True, k=1.4, alpha=1.0, node_shape='o', node_labels=None, node_size_factor=5, seed=1, unique_countries=None, websiteNetworkCountries=None):
    # nx.draw_spring(G, with_labels=with_labels, alpha = alpha)
    d = dict(G.degree)
    
    pos = nx.spring_layout(G, k=k, seed=seed, weight=tuple([d[k]*node_size_factor for k in d.keys()]))
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.15, color='white'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        textposition='top center',
        marker=dict(
            showscale=True,
            colorscale='Hot',
            reversescale=False,
            color=[],
            size=[node_size_factor*np.log([d[k] for k in d.keys()])[i] for i in range(len(node_x))],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=0.2, color='black')  # Remove the line around each node
        ),
        texttemplate=unique_countries,
        textfont=dict(
            size=[7 for i in range(len(node_x))]
        ),
        hovertext=websiteNetworkCountries[["Country", "Degree", "Closeness centrality", "Katz centrality", "PageRank centrality"]].apply(lambda row: "<br>".join([f"{col}: {row[col]}" for col in websiteNetworkCountries[["Country", "Degree", "Closeness centrality", "Katz centrality", "PageRank centrality"]].columns]), axis=1)
    )

    node_adjacencies = []
    node_text = []
    country_names = unique_countries
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(country_names[node] + ': ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            width=1000,
            height=1000,
            title='Earth map made by the aliens',
            titlefont_size=16,
            title_x=0.45,  # Set the title position to the center
            title_y=0.99,  # Set the title position to the top
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    center_x = 0
    center_y = 0
    radius_4 = 1.1
    fig.add_shape(
        type="circle",
        x0=center_x - radius_4,
        y0=center_y - radius_4,
        x1=center_x + radius_4,
        y1=center_y + radius_4,
        line=dict(color="black", width=0.5),
        fillcolor='rgba(255, 255, 0, 0.1)',
        layer='below',
    )

    fig.show()
    
    return G