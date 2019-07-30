from flask_restful import Resource, reqparse
from flaskr.handlers.giphy_handler import giphy_search, giphy_get_images


class GiphySearch(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("input",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def get(self, input):
        try:
            results = giphy_search(input)
        except:
            return {'message': 'a search error occurred'}, 500

        if results:
            return results, 200
        return {'message': 'Results not found'}, 404


class GiphyGet(Resource):
    def get(self):
        # return {'categories': [category.json() for category in CategoryModel.query.all()]}
        pass

