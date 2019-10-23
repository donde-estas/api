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


def create_person(link, first_name, last_name, missing_n, contact_n):
    """Creates a new missing person in the database."""
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "missing_number": missing_n,
        "contact_number": contact_n
    }
    return requests.post(f'{link}/person', params=payload).json()


def get_person(link, id_):
    """Gets a specific missing person."""
    return requests.get(f'{link}/person/{id_}').json()


def delete_person(link, id_, plain_key):
    """Deletes a specific missing person."""
    payload = {
        "plain_key": plain_key
    }
    return requests.delete(f'{link}/person/{id_}', params=payload).json()


def find_missing(link, id_, plain_key):
    """Sets a specific missing person as found."""
    payload = {
        "plain_key": plain_key
    }
    return requests.patch(f'{link}/missing/{id_}', params=payload).json()


def get_all_found(link):
    """Gets all found persons."""
    return requests.get(f'{link}/found').json()


if __name__ == "__main__":
    LINK = "http://0.0.0.0:5000"
    # LINK = "http://donde-estas.herokuapp.com"
    COMMANDS = {
        "wake_up":            wake_up,
        "get_all_missing":    get_all_missing,
        "create_new_missing": create_new_missing,
        "get_missing":        get_missing,
        "delete_missing":     delete_missing,
        "find_missing":       find_missing,
        "get_all_found":      get_all_found
    }
    try:
        RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    except IndexError:
        if len(sys.argv) <= 1:
            print("\n\n\n\tInvalid script call. To use the script, run:")
            print("\tpython3 ghost_client.py command *args")
            print("\tWhere *args are the arguments separated by space and "
                  "command corresponds to one of the following:")
            print(f'\t\t{", ".join(COMMANDS.keys())}\n\n')
            sys.exit(1)
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
