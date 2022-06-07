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
import time
from multiprocessing import Process

import requests

from faas_sdk_python import start_server, find_free_port


def test_start_server():
    source = pathlib.Path.cwd() / "tests" / "test_functions" / "http_request" / "main.py"
    name = "http_function"
    port = find_free_port()
    p = Process(target=start_server, args=(name, source, "localhost", port))
    p.start()
    time.sleep(1.0)
    url = 'http://localhost:{port!s}'.format(port=port)
    res = requests.post(url, json={"mode": "SUCCESS"})
    assert res.text == 'success'
    assert res.status_code == 200
    p.terminate()
    p.join()
