# This function calculates the number of undirected edges in a matrix representation of a graph 'g'. It iterates over the matrix, checking for pairs of nodes where the connection is mutual (i.e., an edge exists in both directions). Each undirected edge is counted as 0.5 to avoid double counting when summed

def get_n_undirected(g):
    total = 0
    for i in range(g.shape[0]):
        for j in range(g.shape[0]):
            if (g[i, j] == 1) and (g[i, j] == g[j, i]):
                total += .5
    return total