"""
programmatic drawio export

Copyright 2021 ipydrawio contributors
Copyright 2020 jupyterlab-drawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from ._version import __version__
from .serverextension import load_jupyter_server_extension

__all__ = [
    "load_jupyter_server_extension",
    "_jupyter_server_extension_paths",
    "__version__",
]


def _jupyter_server_extension_paths():
    return [{"module": "ipydrawio_export"}]
