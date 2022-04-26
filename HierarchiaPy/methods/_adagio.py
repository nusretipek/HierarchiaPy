import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def adagio(self, preprocessing=False, plot_network=False, rank='topological'):
    mat = self.mat.astype('int64')

    if preprocessing:
        mat = mat - np.transpose(mat)
        mat = np.where(mat < 0, 0, mat)

    network_graph = nx.from_numpy_matrix(mat, create_using=nx.DiGraph(directed=True))

    if plot_network:
        nx.draw_networkx(network_graph, arrows=True)
        plt.show()

    largest = max(nx.strongly_connected_components(network_graph), key=len)
    while len(largest) > 1:
        sliced_mat = mat[list(largest), :][:, list(largest)]
        min_edges = np.where(sliced_mat == np.min(sliced_mat[sliced_mat > 0]))

        for idx in range(len(min_edges[0])):
            network_graph.remove_edge(list(largest)[min_edges[0][idx]], list(largest)[min_edges[1][idx]])

        largest = max(nx.strongly_connected_components(network_graph), key=len)

    if rank == 'topological':
        return {element: idx for idx, element in enumerate(list(nx.topological_sort(network_graph)))}
    elif rank == 'top':
        level_ranked = []
        rank_dict = {}
        i = 0
        topologically_sorted_nodes = list(nx.topological_sort(network_graph))
        while len(topologically_sorted_nodes) > 0:
            if len(list(network_graph.predecessors(topologically_sorted_nodes[0]))) == 0:
                rank_dict[topologically_sorted_nodes[0]] = i
                topologically_sorted_nodes.pop(0)
            else:
                if not all([True if _ in rank_dict else False for _ in
                            list(network_graph.predecessors(topologically_sorted_nodes[0]))]):
                    i += 1
                    for element in level_ranked:
                        rank_dict[element] = i
                    level_ranked = []
                else:
                    level_ranked.append(topologically_sorted_nodes[0])
                    topologically_sorted_nodes.pop(0)
        for element in level_ranked:
            rank_dict[element] = i + 1
        return rank_dict
    elif rank == 'bottom':
        level_ranked = []
        rank_dict = {}
        i = 0
        topologically_sorted_nodes = list(nx.topological_sort(network_graph))[::-1]
        while len(topologically_sorted_nodes) > 0:
            if len(list(network_graph.successors(topologically_sorted_nodes[0]))) == 0:
                rank_dict[topologically_sorted_nodes[0]] = i
                topologically_sorted_nodes.pop(0)
            else:
                if not all([True if _ in rank_dict else False for _ in
                            list(network_graph.successors(topologically_sorted_nodes[0]))]):
                    i += 1
                    for element in level_ranked:
                        rank_dict[element] = i
                    level_ranked = []
                else:
                    level_ranked.append(topologically_sorted_nodes[0])
                    topologically_sorted_nodes.pop(0)
        i += 1
        for element in level_ranked:
            rank_dict[element] = i
        return {key: abs(rank_dict[key] - i) for key in rank_dict}
    else:
        raise ValueError('Enter a valid rank: ["topological", "top", "bottom"]')
