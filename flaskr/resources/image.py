from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flaskr.models.image import ImageModel


class Image(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("external_id",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    # @jwt_required()
    def get(self, external_id):
        try:
            image = ImageModel.find_by_external_id(external_id)
        except:
            return {'message': 'an error occurred'}, 500

        if image:
            return image.json(), 200
        return {'message': 'Image not found'}, 404

    def post(self, external_id):
        if ImageModel.find_by_external_id(external_id):
            return {
                       "message": f"A image with id '{external_id}' already exists."
                   }, 400

        image = ImageModel(external_id)

        try:
            image.save_to_db()
        except:
            return {'message': 'an error occurred inserting the image'}, 500

        return image.json(), 201

    def delete(self, external_id):
        image = ImageModel.find_by_external_id(external_id)

        if image:
            image.delete_from_db()

        return {'message': f'image {external_id} deleted'}


class ImageList(Resource):
    def get(self):
        return {'images': [image.json() for image in ImageModel.query.all()]}

