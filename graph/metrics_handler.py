import networkx as nx
import matplotlib.pyplot as plt
import matplotlib


class AdjacencyTable:
    def __init__(self, adjacency_matrix, node_ids=None):
        self.adjacency_matrix = adjacency_matrix
        self.node_ids = node_ids if node_ids else {i: i for i in range(len(adjacency_matrix))}
        self.row_dict = self.create_row_dict()
        # self.column_dict = self.create_column_dict()

    def create_row_dict(self):
        row_dict = {}
        for node_id, node_index in self.node_ids.items():
            row_dict[node_id] = [i for i, val in enumerate(self.adjacency_matrix[node_index]) if val == 1]
        return row_dict

    def add_node(self, connections, node_id):
        if len(connections) != len(self.adjacency_matrix):
            print("Error: Number of connections does not match the matrix size.")
            return
        for i in range(len(self.adjacency_matrix)):
            #self.adjacency_matrix[i].append(connections[i])
            # assuming no connections to the new node
            self.adjacency_matrix[i].append(0)
            cur_node_id = list(self.node_ids.keys())[list(self.node_ids.values()).index(i)]
            #if connections[i] == 1:
            #self.row_dict[cur_node_id].append(len(self.adjacency_matrix))
            #self.row_dict[cur_node_id].append(0)
        self.adjacency_matrix.append(connections + [0])
        self.node_ids[node_id] = len(self.adjacency_matrix) - 1
        self.row_dict[node_id] = [i for i in range(len(connections)) if connections[i] == 1]

    def remove_node(self, node_id):
        if node_id not in self.node_ids:
            print("Error: Node ID does not exist.")
            return
        node_index = self.node_ids[node_id]
        del self.node_ids[node_id]
        del self.row_dict[node_id]
        del self.adjacency_matrix[node_index]
        for row in self.adjacency_matrix:
            del row[node_index]
        for key in self.row_dict:
            for i in range(len(self.row_dict[key])):
                if self.row_dict[key][i] == node_index:
                    del self.row_dict[key][i]
                    break
        for key in self.node_ids:
            if self.node_ids[key] > node_index:
                self.node_ids[key] -= 1

    def visualize_graph(self):
        G = nx.DiGraph()
        for node_id, node_index in self.node_ids.items():
            G.add_node(node_id)
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] == 1:
                    node_id1 = list(self.node_ids.keys())[list(self.node_ids.values()).index(i)]
                    node_id2 = list(self.node_ids.keys())[list(self.node_ids.values()).index(j)]
                    G.add_edge(node_id1, node_id2)
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, font_weight='bold',
                arrows=True)
        plt.show()

# matplotlib.use('TkAgg')
#
#
# adjacency_matrix = [
#     [0, 1, 1],
#     [1, 0, 0],
#     [0, 0, 0]
# ]
# node_ids = {'A': 0, 'B': 1, 'C': 2}
# adj_table = AdjacencyTable(adjacency_matrix, node_ids)
#
#
# new_connections = [1, 0, 1]
# adj_table.add_node(new_connections, 'D')
#
# print(adj_table.adjacency_matrix)
# print(adj_table.row_dict)
#
#
# adj_table.remove_node('B')
#
# print(adj_table.adjacency_matrix)
# print(adj_table.row_dict)
# print(adj_table.node_ids)
#
# adj_table.visualize_graph()