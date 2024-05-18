from castle import GraphDAG, MetricsDAG
from castle.algorithms import PC, GES
from graph.metrics_handler import AdjacencyTable

import matplotlib
from castle.datasets import DAG, IIDSimulation

from utils.get_n_undirected import get_n_undirected

matplotlib.use('TkAgg')

results = {}

true_dag = DAG.scale_free(n_nodes=100, n_edges=200)

dataset = IIDSimulation(
    W=true_dag,
    n=500,
    method='linear',
    sem_type='exp')

X = dataset.X

model = PC('parallel')
model.learn(X)
pred_dag = model.causal_matrix
# print(pred_dag)
# node_ids = {}
# adj_table = AdjacencyTable(pred_dag, node_ids)
# adj_table.visualize_graph()

# Get n undir edges
n_undir = get_n_undirected(pred_dag)

# Plot results
GraphDAG(pred_dag, true_dag, 'result')

mt = MetricsDAG(pred_dag, true_dag)
print(
    f'FDR: {mt.metrics["fdr"]}')  # FDR shows the proportion of false positive reltionships among all; the lower - the better
print(
    f'Recall: {mt.metrics["recall"]}')  # Recall measures the proportion of actual positive relationships that were correctly identified as such by the model
print(
    f'Precision: {mt.metrics["precision"]}')  # This metric assesses the proportion of predicted positive relationships that are true positives.
print(f'F1 score: {mt.metrics["F1"]}')
print(f'No. of undir. edges: {n_undir}\n')
print('-' * 50, '\n')
