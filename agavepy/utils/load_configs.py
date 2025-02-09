"""
    load_configs.py
"""
from __future__ import print_function
import errno
import json
import os
from .paths import (sessions_cache_path)


def load_config(cache_dir, tenant_id, username, client_name):
    """ Load configurations from file

    Load configuration information from file, if it exists.
    These function will look for the file config.json to restore a session.

    PARAMETERS
    ----------
    cache_dir: string
        Path to store session configuration.
    tenant_id: string
    username: string
    client_name: string

    RETURNS
    -------
    current_context: dict
        Dictionary with client name as key and session context as value.
    """
    # Configuration info will be stored by default in this file.
    config_file = sessions_cache_path(cache_dir)

    # Read in configuration from cache dir if it exist, raise an exception.
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            agave_context = json.load(f)
    else:
        raise IOError(
            errno.ENOENT, os.strerror(errno.ENOENT), config_file)

    # Return the current session context if no extra parameters are passed.
    if client_name in agave_context['current']:
        current = agave_context['current'][client_name]
        if current.get('tenantid', '') == tenant_id and \
                current.get('username', '') == username:
            return client_name, current
    elif tenant_id is None or username is None or client_name is None:
        client_name = list(agave_context['current'])[0]
        return client_name, agave_context['current'][client_name]
    else:
        return client_name, \
            agave_context['sessions'][tenant_id][username][client_name]
