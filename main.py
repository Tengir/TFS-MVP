from castle import GraphDAG
from castle.algorithms import PC

from data.dataset import Dataset
from drafts.pc_dataset_example import PCDatasetExample
from date_time.date_time import DateTime
import matplotlib

from graph.metrics_handler import AdjacencyTable
from utils.get_max_min_datetime import get_max_min_datetime
from utils.save_data_to_txt import save_data_to_txt

# Кол-во используемых ядер для алгоритма.
p_cores=6

matplotlib.use('TkAgg')

ds = Dataset(r"C:\Users\Tengir\Desktop\tfs_20")


get_max_min_datetime(ds)
# 2021-07-07 06:55:32.108421
# 2023-06-10 14:53:47.780689

pcds = PCDatasetExample(ds, DateTime(2023, 6, 6), DateTime(2023, 6, 7))
#print(len(pcds.keys))
#save_data_to_txt(pcds.table, r"C:\Users\Tengir\Desktop\tfs_table.txt")
pc = PC('parallel') # Лучший вариант алгоритма, который работает паралельно.
pc.learn(pcds.table, p_cores=p_cores)

# plot predict_dag
# GraphDAG(pc.causal_matrix)

pred_dag = pc.causal_matrix
print(pred_dag)
node_ids = {}
adj_table = AdjacencyTable(pred_dag, node_ids)
adj_table.visualize_graph()

