"""
Implements the functions necessary to access every donde-estas-api
server function without actually needing a visual interface.
"""


import sys
import json
import requests


def wake_up(link):
    """Wakes up the server by asking for its root page."""
    return requests.get(link)


def get_all_missing(link):
    """Gets all missing persons."""
    return requests.get(link + 'missing').json()


def create_new_missing(link, first_name, last_name, missing_n, contact_n):
    """Creates a new missing person in the database."""
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "missing_number": missing_n,
        "contact_number": contact_n
    }
    return requests.post(link + 'missing', params=payload).json()


if __name__ == "__main__":
    LINK = "http://0.0.0.0:5000/"
    # LINK = ""
    COMMANDS = {
        "wake_up":            wake_up,
        "get_all_missing":    get_all_missing,
        "create_new_missing": create_new_missing
    }
    RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
