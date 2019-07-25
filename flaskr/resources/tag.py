from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flaskr.models.tag import TagModel


class Tag(Resource):

    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        try:
            tag = TagModel.find_by_name(name)
        except:
            return {'message': 'an error occurred'}, 500

        if tag:
            return tag.json(), 200
        return {'message': 'Tag not found'}, 404

    def post(self, name):
        if TagModel.find_by_name(name):
            return {
                       "message": f"A tag with name '{name}' already exists."
                   }, 400

        data = Tag.parser.parse_args()
        tag = TagModel(name, **data)

        try:
            tag.save_to_db()
        except:
            return {'message': 'an error occurred inserting the tag'}, 500

        return tag.json(), 201

    def delete(self, name):
        tag = TagModel.find_by_name(name)

        if tag:
            tag.delete_from_db()

        return {'message': f'tag {name} deleted'}

    def put(self, name):
        data = Tag.parser.parse_args()  # data = request.get_json()
        try:
            tag = TagModel.find_by_name(name)
        except:
            return {'message': 'an error occurred'}, 500

        if tag is None:
            tag = TagModel(name, **data)
        else:
            tag.price = data['price']


        try:
            tag.save_to_db()
        except:
            return {'message': 'an error occurred updating tag'}, 500

        return tag.json()


class TagList(Resource):
    def get(self):
        return {'tags': [tag.json() for tag in TagModel.query.all()]}

