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

import importlib.util
import os
import sys
import types

from faas_sdk_python.exceptions import MissingTargetException, InvalidTargetTypeException


def get_user_function(source, source_module, target):
    """Returns user function, raises exception for invalid function."""
    # Extract the target function from the source file
    if not hasattr(source_module, target):
        raise MissingTargetException(
            "File {source} is expected to contain a function named '{target}'".format(
                source=source, target=target
            )
        )
    function = getattr(source_module, target)
    # Check that it is a function
    if not isinstance(function, types.FunctionType):
        raise InvalidTargetTypeException(
            "The function defined in file {source} as {target} needs to be of "
            "type function. Got: invalid type {target_type}".format(
                source=source, target=target, target_type=type(function)
            )
        )
    return function


def load_function_module(source):
    """Load user function source file."""
    # 1. Extract the module name from the source path
    realpath = os.path.realpath(source)
    directory, filename = os.path.split(realpath)
    name, extension = os.path.splitext(filename)
    # 2. Create a new module
    spec = importlib.util.spec_from_file_location(
        name, realpath, submodule_search_locations=[directory]
    )
    source_module = importlib.util.module_from_spec(spec)
    # 3. Add the directory of the source to sys.path to allow the function to
    # load modules relative to its location
    sys.path.append(directory)
    # 4. Add the module to sys.modules
    sys.modules[name] = source_module
    return source_module, spec