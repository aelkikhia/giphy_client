from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flaskr.models.category import CategoryModel


class Category(Resource):

    parser = reqparse.RequestParser()

    # @jwt_required()
    def get(self, name):
        try:
            category = CategoryModel.find_by_name(name)
        except:
            return {'message': 'an error occurred'}, 500

        if category:
            return category.json(), 200
        return {'message': 'Category not found'}, 404

    def post(self, name):
        if CategoryModel.find_by_name(name):
            return {
                       "message": f"A category with name '{name}' already exists."
                   }, 400

        # data = Category.parser.parse_args()
        category = CategoryModel(name)

        try:
            category.save_to_db()
        except:
            return {'message': 'an error occurred inserting the category'}, 500

        return category.json(), 201

    def delete(self, name):
        category = CategoryModel.find_by_name(name)

        if category:
            category.delete_from_db()

        return {'message': f'category {name} deleted'}

    def put(self, name):
        data = Category.parser.parse_args()  # data = request.get_json()
        try:
            category = CategoryModel.find_by_name(name)
        except:
            return {'message': 'an error occurred'}, 500

        if category is None:
            category = CategoryModel(name)
        else:
            category.price = data['price']


        try:
            category.save_to_db()
        except:
            return {'message': 'an error occurred updating category'}, 500

        return category.json()


class CategoryList(Resource):
    def get(self):
        return {'categories': [category.json() for category in CategoryModel.query.all()]}

