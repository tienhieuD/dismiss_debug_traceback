# -*- coding: utf-8 -*-
import functools
import json

import werkzeug

from odoo import http
from odoo.http import _logger, serialize_exception as _serialize_exception
from odoo.addons.web.controllers import main


def http_serialize_exception(e):
    tmp = _serialize_exception(e)
    tmp['debug'] = tmp['name']
    return tmp


def web_serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            _logger.exception("An exception occurred during an http request")
            se = http_serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(json.dumps(error))

    return wrap


# Monkey patching
http.serialize_exception = http_serialize_exception
main.serialize_exception = web_serialize_exception
