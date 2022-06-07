# Copyright 2022 АО «СберТех»
#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import socket
from contextlib import closing

import flask
import werkzeug

from faas_sdk_python import _function_registry
from faas_sdk_python._function_registry import load_function_module, get_user_function


def _http_view_func_wrapper(function, request):
    def view_func():
        return function(request._get_current_object())

    return view_func


def _configure_app(app, function):
    # Mount the function at the root.
    # Modify the url_map and view_functions directly here instead of using
    # add_url_rule in order to create endpoints that route all methods
    app.url_map.add(
        werkzeug.routing.Rule("/", endpoint="run")
    )
    app.view_functions["run"] = _http_view_func_wrapper(function, flask.request)
    app.register_error_handler(500, lambda e: ("generic error occurred", 500))
    app.after_request(read_request)


def read_request(response):
    """
    Force the framework to read the entire request before responding, to avoid
    connection errors when returning prematurely.
    """

    flask.request.get_data()
    return response


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def start_server(function_name, function_source, host="localhost", port=None):
    app = create_app(function_name, function_source)
    if not port:
        port = find_free_port()

    print("Running function: {}".format(function_name))
    app.run(host, port)


def create_app(function_name=None, source=None):
    if not os.path.exists(source):
        raise FileNotFoundError(
            "File {file} with function source doesn't exist".format(
                file=source
            )
        )

    source_module, spec = load_function_module(source)

    _app = flask.Flask(function_name)

    # Execute the module, within the application context
    with _app.app_context():
        spec.loader.exec_module(source_module)

    function = get_user_function(source, source_module, function_name)
    _configure_app(_app, function)

    return _app
