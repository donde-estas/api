"""
Implements the functions necessary to access every donde-estas-api
server function without actually needing a visual interface.
"""


import sys
import json
import requests


def wake_up(link):
    """Wakes up the server by asking for its root page."""
    return requests.get(f'{link}/')


def get_all_missing(link):
    """Gets all missing persons."""
    return requests.get(f'{link}/missing').json()


def create_new_missing(link, first_name, last_name, missing_n, contact_n):
    """Creates a new missing person in the database."""
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "missing_number": missing_n,
        "contact_number": contact_n
    }
    return requests.post(f'{link}/missing', params=payload).json()


def get_missing(link, id_):
    """Gets a specific missing person."""
    return requests.get(f'{link}/missing/{id_}').json()


def delete_missing(link, id_, plain_key):
    """Deletes a specific missing person."""
    payload = {
        "plain_key": plain_key
    }
    return requests.delete(f'{link}/missing/{id_}', params=payload).json()


if __name__ == "__main__":
    LINK = "http://0.0.0.0:5000"
    # LINK = "http://donde-estas.herokuapp.com"
    COMMANDS = {
        "wake_up":            wake_up,
        "get_all_missing":    get_all_missing,
        "create_new_missing": create_new_missing,
        "get_missing":        get_missing,
        "delete_missing":     delete_missing
    }
    RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
