import os
import json
import numpy as np
from .utils import generate_uuid

class SLHDAMVP:
    """Scalar-Ledger Hybrid Data Architecture (MVP)"""
    def __init__(self, store_path="scalar.bin", ledger_path="ledger.json"):
        self.store_path = store_path
        self.ledger_path = ledger_path
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                self.ledger = json.load(f)
        else:
            self.ledger = {}
        if not os.path.exists(self.store_path):
            with open(self.store_path, 'wb') as f:
                pass

    def _append_scalars(self, values):
        with open(self.store_path, 'ab') as f:
            np.array(values, dtype=np.float64).tofile(f)
        start = self._get_store_length() - len(values)
        return start

    def _get_store_length(self):
        return os.path.getsize(self.store_path)//8 if os.path.exists(self.store_path) else 0

    def store_object(self, values, shape, tags=[]):
        start = self._append_scalars(values)
        obj_id = generate_uuid()
        self.ledger[obj_id] = {
            "start": start,
            "length": len(values),
            "shape": shape,
            "tags": tags
        }
        self._save_ledger()
        return obj_id

    def get(self, object_id):
        if object_id not in self.ledger:
            raise ValueError(f"Object {object_id} not found.")
        entry = self.ledger[object_id]
        with open(self.store_path, 'rb') as f:
            f.seek(entry["start"]*8)
            data = np.fromfile(f, dtype=np.float64, count=entry["length"])
        return data.reshape(entry["shape"])

    def set_shape(self, object_id, new_shape):
        if object_id not in self.ledger:
            raise ValueError(f"Object {object_id} not found.")
        self.ledger[object_id]["shape"] = new_shape
        self._save_ledger()

    def alias(self, existing_id, new_shape, new_tags=[]):
        if existing_id not in self.ledger:
            raise ValueError(f"Object {existing_id} not found.")
        entry = self.ledger[existing_id]
        obj_id = generate_uuid()
        self.ledger[obj_id] = {
            "start": entry["start"],
            "length": entry["length"],
            "shape": new_shape,
            "tags": new_tags
        }
        self._save_ledger()
        return obj_id

    def query(self, tag):
        return [obj_id for obj_id, entry in self.ledger.items() if tag in entry["tags"]]

    def _save_ledger(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)