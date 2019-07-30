from flaskr.db import db


class ImageModel(db.Model):

    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    # TODO decide on proper length for giphy alpha-numeric ids
    external_id = db.Column(db.String(80))

    def __init__(self, external_id):
        self.external_id = external_id

    def json(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
        }

    @classmethod
    def find_by_external_id(cls, external_id):
        return cls.query.filter_by(external_id=external_id).first()

    def save_to_db(self):
        """ replaces insert and update"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
