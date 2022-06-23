import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import warnings


def directed_network_graph(self, **kwargs):
    processed_mat = self.mat - np.transpose(self.mat)
    processed_mat = np.where(processed_mat < 0, 0, processed_mat)

    # Network graph
    plot_processed_mat = (processed_mat / processed_mat.sum()).round(decimals=4)
    network_graph = nx.from_numpy_matrix(plot_processed_mat, create_using=nx.DiGraph(directed=True))
    network_graph = nx.relabel_nodes(network_graph, {idx: name for idx, name in enumerate(self.indices)})
    network_graph_int = nx.from_numpy_matrix(processed_mat, create_using=nx.DiGraph(directed=True))
    network_graph_int = nx.relabel_nodes(network_graph_int, {idx: name for idx, name in enumerate(self.indices)})

    if 'fig_size' in kwargs:
        figure = plt.figure(figsize=kwargs['fig_size'])
        del kwargs['fig_size']
    else:
        figure = plt.figure()

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
        weights_final = {key: (weights_int[key], weights[key]) for key in weights}
        nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=weights_final)
        plt.tight_layout()
        figure.canvas.draw()
        return figure

    except:
        warnings.warn('Layout is not suitable for planar!')
        return None
