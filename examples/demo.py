import numpy as np
from slhda_mvp.store import SLHDAMVP
from slhda_mvp.interpreter import Interpreter
import time

db = SLHDAMVP()
interp = Interpreter(db)

# Multi-scale simulation
grid_data = np.random.rand(16).tolist()
obj_id = db.store_object(grid_data, shape=[4,4], tags=["simulation","grid"])
print("Grid 4x4:", interp.retrieve(obj_id))

# Tensor aliasing
vector_id = interp.alias(obj_id, new_shape=[16], new_tags=["vector"])
print("Vector alias:", interp.retrieve(vector_id))

subgrid_id = interp.alias(obj_id, new_shape=[2,2,4], new_tags=["subgrid"])
print("Subgrid alias:", interp.retrieve(subgrid_id))

# Semantic query
pressure_id = db.store_object(np.random.rand(16).tolist(), shape=[4,4], tags=["pressure","simulation"])
sim_ids = db.query("simulation")
print("Simulation object IDs:", sim_ids)

# Batch retrieval
batch = interp.batch_query("simulation")
print("Batch shapes:", [arr.shape for arr in batch])

# Performance test
N = 10**6
perf_id = db.store_object(np.random.rand(N).tolist(), shape=[N], tags=["perf"])
start = time.time()
retrieved = interp.retrieve(perf_id)
end = time.time()
print(f"Retrieved 1M scalars in {end-start:.4f} seconds")