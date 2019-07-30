from flaskr.db import db

user_image = db.Table('user_like_image',
                      db.Column(
                          'user_id', db.Integer, db.ForeignKey('user.id'),
                          primary_key=True),
                      db.Column(
                          'image_id', db.Integer, db.ForeignKey('image.id'),
                          primary_key=True)
                      )


class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(80))
    likes = db.relationship('ImageModel',
                            secondary=user_image,
                            backref=db.backref('likes', lazy='dynamic'))

    def __init__(self, external_id):
        self.external_id = external_id

    @classmethod
    def find_by_external_id(cls, external_id):
        return cls.query.filter_by(external_id=external_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        """ replaces insert and update"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

