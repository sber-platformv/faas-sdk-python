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

import click
import os

from faas_sdk_python import start_server


@click.command()
@click.option("--target", envvar="target", type=click.STRING, required=True)
@click.option("--source", envvar="source", type=click.Path(), default=os.path.realpath("./handler.py"))
@click.option("--host", envvar="HOST", type=click.STRING, default="0.0.0.0")
@click.option("--port", envvar="PORT", type=click.INT, default=8080)
@click.option("--dry-run", envvar="DRY_RUN", is_flag=True, default=False)
def _cli(target, source, host, port, dry_run):
    if dry_run:
        click.echo("Function: {}".format(target))
        click.echo("URL: http://{}:{}/".format(host, port))
        click.echo("Dry run successful, shutting down.")
    else:
        start_server(target, source, host, port)
