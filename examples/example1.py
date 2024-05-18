from castle import GraphDAG, MetricsDAG
from castle.algorithms import PC, GES

import matplotlib
from castle.datasets import DAG, IIDSimulation

from utils.get_n_undirected import get_n_undirected

matplotlib.use('TkAgg')


methods = {
    'PC': PC,
    'GES': GES
}

results = {}

true_dag = DAG.scale_free(n_nodes=10, n_edges=15, seed=18)


DATA_PARAMS = {
    'linearity': ['linear', 'nonlinear'],
    'distribution': {
        'linear': ['gauss', 'exp'],
        'nonlinear': ['quadratic']
    }
}

datasets = {}

for linearity in DATA_PARAMS['linearity']:
    for distr in DATA_PARAMS['distribution'][linearity]:

        datasets[f'{linearity}_{distr}'] = IIDSimulation(
            W=true_dag,
            n=2000,
            method=linearity,
            sem_type=distr)

for k, dataset in datasets.items():
    try:
        print(f'************* Current dataset: {k}\n')
        X = dataset.X

        results[dataset] = {}
        for method in methods:
            print(f'Method: {method}')
            model = methods[method]()
            model.learn(X)
            pred_dag = model.causal_matrix

            # Get n undir edges
            n_undir = get_n_undirected(pred_dag)

            # Plot results
            GraphDAG(pred_dag, true_dag, 'result')

            mt = MetricsDAG(pred_dag, true_dag)
            print(f'FDR: {mt.metrics["fdr"]}') #FDR shows the proportion of false positive reltionships among all; the lower - the better
            print(f'Recall: {mt.metrics["recall"]}') # Recall measures the proportion of actual positive relationships that were correctly identified as such by the model
            print(f'Precision: {mt.metrics["precision"]}') #This metric assesses the proportion of predicted positive relationships that are true positives.
            print(f'F1 score: {mt.metrics["F1"]}')
            print(f'No. of undir. edges: {n_undir}\n')
            print('-' * 50, '\n')

            results[dataset][method] = pred_dag

        print('\n')
    except:
        print("", end="")