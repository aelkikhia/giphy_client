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
                        required=False,
                        help="This field cannot be left blank.")

    def post(self):
        """user (un)likes an image
        find user and image. if image does not exist add it. create or
        remove relationship
        TODO: do not remove relationship, just deactivate and update time
        :return: response message and code
        """
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
            # TODO: add user/image association to bypass the below sql call

        query_user_image = UserModel.query.join(user_image).join(ImageModel).filter(
            (user_image.c.user_id == user.id) &
            (user_image.c.image_id == image.id)).all()

        # TODO: break into smaller functions for reusability
        if query_user_image:
            user.likes.remove(image)
            user.save_to_db()
            return {'message': 'Image unliked successfully.'}, 201
        else:
            user.likes.append(image)
            user.save_to_db()
            return {'message': 'Image liked successfully.'}, 201

    def get(self):
        """ get a list of all users liked image ids"""
        data = UserImage.parser.parse_args()

        user = UserModel.find_by_external_id(data['external_user_id'])

        if not user:
            return {'message': 'No user with that ID exists'}, 404

        return {'likes': user.likes}









