from ki import db
from json import dumps


class Trees(db.Model):
    __tablename__ = "trees"
    id = db.Column(db.Integer(), primary_key=True)
    x = db.Column(db.Float(), nullable=False)
    y = db.Column(db.Float(), nullable=False)
    data = db.Column(db.JSON())
    reserved = db.Column(db.Boolean(), server_default="0")
    reserved_at = db.Column(db.Date())
    reserved_by = db.Column(db.String(100))

    def jsonify(self, only_coords):
        data = self.data
        data["x"] = self.x
        data["y"] = self.y
        return dumps(data)

    @staticmethod
    def parse(obj: dict):
        """Parses json objects to """

        tree = Trees(x=obj["coords"][0], y=obj["coords"][0])
        obj.pop("coords")
        tree.data = obj
        return tree

    def __repr__(self):
        return f"<tree {self.id} {self.lang}/{self.lang}>"


class PLZ(db.Model):
    __tablename__ = "plz"
    id = db.Column(db.Integer(), primary_key=True)
    plz = db.Column(db.Integer())
    x = db.Column(db.Float(), nullable=False)
    y = db.Column(db.Float(), nullable=False)