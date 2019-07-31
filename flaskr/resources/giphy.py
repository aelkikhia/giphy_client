from flask_restful import Resource, reqparse
from flaskr.handlers.giphy_handler import giphy_search, giphy_get_images
from flaskr.models.user import UserModel


class GiphySearch(Resource):
    """generic giphy search """
    parser = reqparse.RequestParser()
    parser.add_argument("search_input",
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument("external_user_id",
                        type=str,
                        required=False)

    def get(self):
        """ get search results from giphy api
        :param search_input:
        :return:
        """

        data = GiphySearch.parser.parse_args()

        try:
            results = giphy_search(data['search_input'])
        except:
            # TODO: log meta data from giphy api data structure on failure e.g.
            # "meta": {
            #     "status": 200,
            #     "msg": "OK",
            #     "response_id": "5d4075024a774a4573ec8a39"
            # }
            return {'message': 'a search error occurred'}, 500

        if not results:
            return {'message': 'Results not found'}, 404

        formatted_results = format_giphy_results(results)

        # # add likes to our data
        if data['external_user_id'] is not None:
            user = UserModel.find_by_external_id(data['external_user_id'])

            if user:
                likes = user.likes
                if likes:
                    set_liked_images_to_results(formatted_results, likes)

        return formatted_results, 200


class GiphyGet(Resource):
    """Search for specific images"""
    def get(self):
        # return {'categories': [category.json() for category in CategoryModel.query.all()]}
        pass


def format_giphy_results(results):
    """format giphy response to a simpler dictionary of images
    :param results:
    :return: dictionary of search results
    """
    formatted_data = {}
    for image in results['data']:
        formatted_data[image['id']] = {
            "id": image['id'],
            'title': image['title'],
            'liked': 0,
            'images': {
                'fixed_width_small': image['images']['fixed_width_small'],
                'original': image['images']['original']
            }
        }

    return {
        'data': formatted_data,
        'pagination': results['pagination']
    }


def set_liked_images_to_results(images, likes):
    """ marks all user likes in the search results
    :param images: dictionary
    :param likes: list
    :return: dictionary
    """
    likes = [str(like) for like in likes]
    for liked_image_id in likes:
        if liked_image_id in images['data'].keys():
            images['data'][liked_image_id]['liked'] = 1

    return images
