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

import pretend as pretend
import pytest


from click.testing import CliRunner

import faas_sdk_python
from faas_sdk_python._cli import _cli


def test_cli_no_arguments():
    runner = CliRunner()
    result = runner.invoke(_cli)

    assert result.exit_code == 2
    assert "Missing option '--function-name'" in result.output


def test_cli_empty_source():
    runner = CliRunner()
    result = runner.invoke(_cli, ["--function-name", "foo"])

    assert result.exit_code == 2
    assert "Missing option '--source'" in result.output


@pytest.mark.parametrize(
    "args, create_app_calls",
    [
        (
                ["--target", "foo", "--source", "/path/to/source.py"],
                [pretend.call("foo", "/path/to/source.py", "0.0.0.0", 8080)]
        ),
        (
                ["--target", "foo", "--source", "/path/to/source.py", "--host", "127.0.0.1"],
                [pretend.call("foo", "/path/to/source.py", "127.0.0.1", 8080)]
        ),
        (
                ["--target", "foo", "--source", "/path/to/source.py", "--port", "1234"],
                [pretend.call("foo", "/path/to/source.py", "0.0.0.0", 1234)]
        ),
        (
                ["--target", "foo", "--source", "/path/to/source.py", "--dry-run"],
                []
        )
    ],
)
def test_cli(monkeypatch, args, create_app_calls):
    wsgi_app = pretend.stub(run=pretend.call_recorder(lambda *a, **kw: None))
    start_server = pretend.call_recorder(lambda *a, **kw: wsgi_app)
    monkeypatch.setattr(faas_sdk_python._cli, "start_server", start_server)

    runner = CliRunner()
    result = runner.invoke(_cli, args)

    assert result.exit_code == 0
    assert start_server.calls == create_app_calls
