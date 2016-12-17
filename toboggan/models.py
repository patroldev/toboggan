from toboggan import db

class Dispatcher(db.Model):
    __table_name__ = 'dispatcher'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
