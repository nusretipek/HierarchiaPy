import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib
import warnings


def directed_network_graph(self, **kwargs) -> matplotlib.figure.Figure:

    """Directed network graph with absolute and proportional win tuples in edges.

    Parameters
    ----------
    :param kwargs: dict
        Pass parameter for fig_size in matplotlib and pass parameters for draw_networkx method.

    Returns
    -------
    figure : matplotlib.figure.Figure
        Planar layout network graph figure. The nodes are named as indices passed to Hierarchia object.
        The edges have absolute and proportional dyadic relationship indicators.

    See also
    --------
    https://networkx.org/documentation/stable/reference/classes/digraph.html
    https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.planar_layout.html
    https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html
    """

    # Process matrix
    processed_mat = self.mat - np.transpose(self.mat)
    processed_mat = np.where(processed_mat < 0, 0, processed_mat)

    # Network graph
    plot_processed_mat = (processed_mat / processed_mat.sum()).round(decimals=4)
    network_graph = nx.from_numpy_matrix(plot_processed_mat, create_using=nx.DiGraph(directed=True))
    network_graph = nx.relabel_nodes(network_graph, {idx: name for idx, name in enumerate(self.indices)})
    network_graph_int = nx.from_numpy_matrix(processed_mat, create_using=nx.DiGraph(directed=True))
    network_graph_int = nx.relabel_nodes(network_graph_int, {idx: name for idx, name in enumerate(self.indices)})

    # Adjust figure size
    if 'fig_size' in kwargs:
        figure = plt.figure(figsize=kwargs['fig_size'])
        del kwargs['fig_size']
    else:
        figure = plt.figure()

    # Try plot the network with planar layout
    try:
        pos = nx.planar_layout(network_graph)
        nx.draw_networkx(network_graph,
                         pos,
                         **kwargs,
                         node_size=1000,
                         linewidths=2,
                         node_shape='8')

        weights = nx.get_edge_attributes(network_graph, 'weight')
        weights_int = nx.get_edge_attributes(network_graph_int, 'weight')
        weights_final = {key: (weights_int[key], round(weights[key], 4)) for key in weights}
        nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=weights_final)
        plt.tight_layout()
        figure.canvas.draw()
        return figure
    except:
        warnings.warn('Layout is not suitable for planar!')
        return None
