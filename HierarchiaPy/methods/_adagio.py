import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def adagio(self, preprocessing=False, plot_network=False, rank='topological'):

    """ADAGIO from an interaction dataframe/matrix.

    Parameters
    ----------
    :param self: reference to the current instance of the class

    :param preprocessing: boolean
        preprocessing of the initial matrix according to the original paper [Douglas, 2016].  For a given dominance
        network, the preprocessed weight of the edge between the individual A that appears dominant and the individual B
        that appears subordinate is set to the difference in the number of interactions won by A and the number
        of interactions won by B. (False)

    :param plot_network: boolean
        Simple network plot of the derived directed graph network from the dataframe/matrix. (False)

    :param rank: str
        Final ranking algorithm after the ADAGIO iterations. Three options are possible; 'topological' that yields
        topological order of the final matrix. 'top' and 'bottom' are self-explanatory and can be found at original
        paper. (topological)

    Returns
    -------
    rank_dict : dict
        Rankings from the ADAGIO algorithm, ranked based on the ranking parameter chosen. 
        Keys are identification of individuals (see name_seq) and the values are the ranks. 

    See also
    --------
    https://networkx.org/documentation/networkx-1.9/reference/generated/networkx.algorithms.components.strongly_connected.strongly_connected_components.html
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_sort.html

    Notes
    -----
    ADAGIO, for assessing the structure of dominance networks. ADAGIO computes dominance hierarchies, in the form of
    directed acyclic graphs, to represent the dominance relations of a given group of animals. Thus far, most
    methods for computing dominance ranks assume implicitly that the dominance relation is a total order
    of the individuals in a group. ADAGIO does not assume or require this to be always true, and is hence
    more appropriate for analysing dominance hierarchies that are not strongly linear. (Douglas, 2017)

    References
    ----------
    * Douglas, P. H., Ngomo, A. C. N., & Hohmann, G. (2017). A novel approach for dominance assessment in gregarious
      species: ADAGIO. Animal Behaviour, 123, 21-32.    

    """

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
            mat[list(largest)[min_edges[0][idx]], list(largest)[min_edges[1][idx]]] = 0

        largest = max(nx.strongly_connected_components(network_graph), key=len)

    if rank == 'topological':
        return {self.indices[element]: idx for idx, element in enumerate(list(nx.topological_sort(network_graph)))}
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
        return {self.indices[element]: rank_dict[element] for element in rank_dict}
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
        rank_dict = {key: abs(rank_dict[key] - i) for key in rank_dict}
        return {self.indices[element]: rank_dict[element] for element in rank_dict}
    else:
        raise ValueError('Enter a valid rank: ["topological", "top", "bottom"]')
