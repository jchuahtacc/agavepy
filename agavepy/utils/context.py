from __future__ import print_function
import errno
import json
import os
from copy import copy
from .paths import (sessions_cache_path, client_cache_path,
                    credentials_cache_dir)

ALLOWED_KEYS = ('tenantid', 'baseurl', 'username', 'apikey',
                'apisecret', 'client_name', 'expires_at',
                'expires_in', 'created_at', 'access_token',
                'refresh_token', 'devurl')

DEFAULT_KEYS = ('tenantid', 'baseurl', 'username',
                'access_token', 'refresh_token', 'apikey', 'apisecret')

__all__ = ['bootstrap_context']


def _context_from_client_file(client_file, context={}, **kwargs):
    context = kwargs
    if os.path.exists(client_file):
        client_obj = json.load(open(client_file, 'rb'))
        for k, kwarg_val in kwargs.items():
            # Sometimes null or None or empty gets stored as "" in JSON
            if kwarg_val == '':
                kwarg_val = None
            if k not in ALLOWED_KEYS:
                raise ValueError('Unknown keyword {0}'.format(k))
            val = client_obj.get(k, None)
            # Allow loaded value to override passed value if not None
            if kwarg_val != val and kwarg_val is None:
                context[k] = val
        return context
    else:
        raise IOError('Sessions file not found')


def _context_from_sessions_file(sessions_file, **kwargs):
    context = kwargs
    if os.path.exists(sessions_file):
        sessions_obj = json.load(open(sessions_file, 'rb')).get('current')
        client_name = list(sessions_obj)[0]
        client_obj = sessions_obj[client_name]
        for k, kwarg_val in kwargs.items():
            # Sometimes null or None or empty gets stored as "" in JSON
            if kwarg_val == '':
                kwarg_val = None
            if k not in ALLOWED_KEYS:
                raise ValueError('Unknown keyword {0}'.format(k))
            val = client_obj.get(k, None)
            # Allow loaded value to override passed value if not None
            if kwarg_val != val and kwarg_val is None:
                context[k] = val
        if context.get('client_name', None) is None or \
                context.get('client_name', None) == '':
            context['client_name'] = client_name
        return context
    else:
        raise IOError('Sessions file not found')


def bootstrap_context(cache_dir=None, precedence='sessions', **kwargs):

    # Populate a reasonable context event if no key names are passed
    if len(kwargs) == 0:
        kwargs = {k: None for k in DEFAULT_KEYS}
    # current
    client_file = client_cache_path(cache_dir)
    # config.json
    sessions_file = sessions_cache_path(cache_dir)

    try:
        client_context = _context_from_client_file(
            client_file, **kwargs)
    except IOError:
        client_context = copy(kwargs)

    try:
        sessions_current_context = _context_from_sessions_file(
            sessions_file, **kwargs)
    except IOError:
        sessions_current_context = copy(client_context)

    if precedence == 'sessions':
        client_context.update(sessions_current_context)
        return client_context
    else:
        sessions_current_context.update(client_context)
        return sessions_current_context
