from .store import SLHDAMVP

class Interpreter:
    """Semantic reconstruction and aliasing layer."""
    def __init__(self, db: SLHDAMVP):
        self.db = db

    def retrieve(self, object_id):
        return self.db.get(object_id)

    def reshape(self, object_id, new_shape):
        self.db.set_shape(object_id, new_shape)
        return self.db.get(object_id)

    def alias(self, object_id, new_shape, new_tags=[]):
        return self.db.alias(object_id, new_shape, new_tags)

    def batch_query(self, tag):
        ids = self.db.query(tag)
        return [self.db.get(obj_id) for obj_id in ids]