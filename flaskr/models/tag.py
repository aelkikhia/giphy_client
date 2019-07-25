from flaskr.db import db


class TagModel(db.Model):

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    gif_id = db.Column(db.Integer, db.ForeignKey('gifs.id'))
    gif = db.relationship('GifModel')

    def __init__(self, name, gif_id):
        self.name = name
        self.gif_id = gif_id

    def json(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """ replaces insert and update"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()