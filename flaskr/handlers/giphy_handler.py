#!/usr/bin/python3

"""API functions for Giphy api"""

import logging

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException

LOGGER = logging.getLogger(__name__)

API_KEY = 'g18Ik9ci8NgkVAjZoRfIyqN90tpjZE9k'
baseURL = f'https://api.giphy.com/v1/gifs/'
rating = 'G'
lang = 'en'
limit = 10


def get_headers(token=None):
    """ return header dictionary for api calls"""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["API_KEY"] = token
    return headers


def api_request(verb, url, data=None, token=None):
    """makes a request and returns the resp or None
    :param verb:
    :param url:
    :param data:
    :param token:
    :return:
    """

    parameters = {
        "headers": get_headers(token),
    }

    if data is not None:
        parameters["data"] = data

    try:
        resp = requests.request(verb, url, **parameters)
    except ConnectionError as err:
        LOGGER.error(f"Connection Error - resp: {err.response}", exc_info=True)
        return None
    except (HTTPError, RequestException) as err:
        LOGGER.error(f"Error: API {verb} {url} - resp: {err.response}",
                     exc_info=True)
        return None
    if resp is None:
        LOGGER.error(f"{verb} {url} - resp is None")
        return None

    LOGGER.debug(f"{verb} {url} - {resp.status_code} - {resp.text}")
    return resp


def get_config(url):
    """Makes a request to the api returns the json response or None
    :param url:
    :return: JSON
    """
    resp = api_request("GET", url)

    if resp is None:
        LOGGER.error("Could not get config json")
        return None

    return resp.json()


def giphy_search(q_input=None):
    """ Takes a search query input string and makes a request to the giphy api
    returning a json response
    :param q_input:
    :return:
    """
    if input is None:
        return {}

    resp = api_request(
        "GET",
        f'{baseURL}search?api_key={API_KEY}&q={q_input}&limit=${limit}&rating={rating}&lang={lang}'
    )
    if resp is None:
        LOGGER.error("Could not get giphy search response")

    return resp.json()


def giphy_get_images():
    pass


if __name__ == "__main__":
    pass
