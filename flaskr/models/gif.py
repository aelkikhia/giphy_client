from flaskr.db import db


class GifModel(db.Model):

    __tablename__ = 'gifs'
    id = db.Column(db.Integer, primary_key=True)
    # TODO decide on proper length for giphy alpha-numeric ids
    giphy_id = db.Column(db.String(80))
    tags = db.relationship('TagModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "giphy_id": self.giphy_id,
            "tags": [tag.json() for tag in self.tag.all()]
        }

    @classmethod
    def find_by_giphy_id(cls, giphy_id):
        return cls.query.filter_by(name=giphy_id).first()

    def save_to_db(self):
        """ replaces insert and update"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
