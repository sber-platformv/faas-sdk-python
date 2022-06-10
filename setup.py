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

from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="faas-sdk-python",
    version="1.0.1",
    description="An open source FaaS (Function as a service) sdk for Sber Platform V functions local testing & running",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sber-platformv/faas-sdk-python",
    author="Sber",
    author_email="developers@sber.ru",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="faas-sdk-python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8, <4",
    install_requires=[
        "flask>=2.0,<3.0",
        "click>=7.0,<9.0",
    ],
    entry_points={
        "console_scripts": [
            "faas-sdk-python=faas_sdk_python._cli:_cli",
            "faas_sdk_python=faas_sdk_python._cli:_cli",
        ]
    },
)
