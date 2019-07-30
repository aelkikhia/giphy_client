from flask_restful import Resource, reqparse
from flaskr.models.user import UserModel, user_image
from flaskr.models.image import ImageModel


class UserImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("external_user_id",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument("external_image_id",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        """ add """
        data = UserImage.parser.parse_args()

        user = UserModel.find_by_external_id(data['external_user_id'])

        if not user:
            return {'message': 'No user with that ID exists'}, 404

        image = ImageModel.find_by_external_id(data['external_image_id'])

        if not image:
            image = ImageModel(data['external_image_id'])
            try:
                image.save_to_db()
            except:
                return {'message': 'an error occurred saving the image'}, 500

        query_user_image = UserModel.query.join(user_image).join(ImageModel).filter(
            (user_image.c.user_id == user.id) & (user_image.c.image_id == image.id)).all()

        print(query_user_image)

        if not query_user_image:
            user.likes.append(image)
            user.save_to_db()
            return {'message': 'Image liked successfully.'}, 201

        return {'message': 'Image already liked by user'}, 400




