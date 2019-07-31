
from flask_restful import Resource, reqparse
from flaskr.models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("external_id",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    # TODO: hook up google auth/jwt
    def post(self):
        """ Create a new user"""
        data = User.parser.parse_args()

        if UserModel.find_by_external_id(data['external_id']):
            return {'message': 'A user with that external_id already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
