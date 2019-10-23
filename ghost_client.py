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


if __name__ == "__main__":
    LINK = "http://0.0.0.0:5000/"
    # LINK = ""
    COMMANDS = {
        "wake_up":                       wake_up,
    }
    RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
