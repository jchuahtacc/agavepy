"""
    list.py

Functions to list agave oauth clients.
"""
from __future__ import print_function
import requests
from .exceptions import AgaveClientError
from ..utils import (handle_bad_response_status_code,
                     get_username, get_password)


def clients_list(tenant_url, username=None, password=None, quiet=False):
    """ List Tapis Oauth clients

    List all Tapis Oauth clients registered to the designated user on
    the specified tenant.

    PARAMETERS
    ----------
    tenant_url: string
        URL of agave tenant to interact with.

    KEYWORD ARGUMENTS
    -----------------
    username: string
        The user's username. If the API username is not passed as a keyword
        argument, it will be retrieved from the environment variable
        TAPIS_USERNAME. If the variable is not set, the user is
        prompted interactively for a value.

    password: string
        The user's password. If the API username is not passed as a keyword
        argument, it will be retrieved from the environment variable
        TAPIS_PASSWORD. If the variable is not set, the user is
        prompted interactively for a value.
    """

    # Get user's credentials
    uname = get_username(username)
    passwd = get_password(password, quiet=quiet)

    # Set request endpoint.
    endpoint = tenant_url + "/clients/v2"

    # Make request.
    try:
        resp = requests.get(endpoint, auth=(uname, passwd))
        del passwd
    except Exception as err:
        del passwd
        raise AgaveClientError(err)

    # Handle bad status code.
    handle_bad_response_status_code(resp)

    # Print results.
    print("{0:<30} {1:<80}".format("NAME", "DESCRIPTION"))
    for client in resp.json().get("result", []):
        description = client["description"] if client["description"] else ""
        print("{0:<30} {1:<80}".format(client["name"], description))
