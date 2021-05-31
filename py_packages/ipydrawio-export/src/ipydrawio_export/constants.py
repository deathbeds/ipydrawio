"""constants for ipydrawio-export"""

# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ipydrawio.constants import IPYNB_METADATA

# the header to look for in PNG metadata
PNG_DRAWIO_INFO = "mxfile"

# TODO: hoist this to `package.json` and consume directly
DRAWIO_APP = "../labextensions/@deathbeds/ipydrawio-webpack/static/dio"

# environment variables
ENV_JUPYTER_DATA_DIR = "JUPYTER_DATA_DIR"
ENV_IPYDRAWIO_DATA_DIR = "IPYDRAWIO_DATA_DIR"

# always appended to *_DATA_DIR
WORK_DIR = "ipydrawio_export"


__all__ = [
    "IPYNB_METADATA",
    "PNG_DRAWIO_INFO",
    "DRAWIO_APP",
    "ENV_JUPYTER_DATA_DIR",
    "ENV_IPYDRAWIO_DATA_DIR",
    "WORK_DIR",
]
