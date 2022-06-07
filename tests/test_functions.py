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

import pathlib
import re

import pytest

from faas_sdk_python import create_app, exceptions

FUNCTIONS_DIR = pathlib.Path.cwd() / "tests" / "test_functions"


@pytest.fixture
def app():
    source = FUNCTIONS_DIR / "http_request" / "main.py"
    function_name = "http_function"
    app = create_app(function_name, source)
    return app


def test_http_function_happy_path(client):
    resp = client.get("/", json={"mode": "SUCCESS"})
    assert resp.status_code == 200
    assert resp.data == b"success"


def test_http_function_executes_failure(client):
    resp = client.get("/", json={"mode": "FAILURE"})
    assert resp.status_code == 400
    assert resp.data == b"failure"


def test_http_function_executes_throw(client):
    resp = client.put("/", json={"mode": "THROW"})
    assert resp.status_code == 500


def test_missing_function_file():
    source = FUNCTIONS_DIR / "invalid_functions" / "init.py"
    target = "function"

    with pytest.raises(FileNotFoundError) as excinfo:
        create_app(target, source)

    assert re.match(
        "File .* with function source doesn't exist", str(excinfo.value)
    )


def test_function_not_found_in_source():
    source = FUNCTIONS_DIR / "invalid_functions" / "main.py"
    function_name = "func"

    with pytest.raises(exceptions.MissingTargetException) as excinfo:
        create_app(function_name, source)

    assert re.match(
        "File .* is expected to contain a function named 'func'", str(excinfo.value)
    )


def test_target_object_is_not_a_function():
    source = FUNCTIONS_DIR / "invalid_functions" / "main.py"
    function_name = "not_a_function"

    with pytest.raises(exceptions.InvalidTargetTypeException) as excinfo:
        create_app(function_name, source)

    assert re.match(
        "The function defined in file .* as not_a_function needs to be of type "
        "function. Got: .*",
        str(excinfo.value),
    )
