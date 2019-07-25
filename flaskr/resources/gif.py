from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flaskr.models.gif import GifModel


class Gif(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, id_):
        try:
            gif = GifModel.find_by_id(id_)
        except:
            return {'message': 'an error occurred'}, 500

        if gif:
            return gif.json(), 200
        return {'message': 'Gif not found'}, 404

    def post(self, id_):
        if GifModel.find_by_id(id_):
            return {
                       "message": f"A gif with id '{id_}' already exists."
                   }, 400

        gif = GifModel(id_)

        try:
            gif.save_to_db()
        except:
            return {'message': 'an error occurred inserting the gif'}, 500

        return gif.json(), 201

    def delete(self, id_):
        gif = GifModel.find_by_id(id_)

        if gif:
            gif.delete_from_db()

        return {'message': f'gif {id_} deleted'}


class GifList(Resource):
    def get(self):
        return {'gifs': [gif.json() for gif in GifModel.query.all()]}

