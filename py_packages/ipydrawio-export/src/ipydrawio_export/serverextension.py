"""add drawio support to a running jupyter application"""

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

import traitlets

from ._version import __version__
from .handlers import add_handlers
from .manager import IPyDrawioExportManager


def load_jupyter_server_extension(app):
    """create a IPyDrawioExportManager and add handlers"""
    app.add_traits(
        drawio_manager=traitlets.Instance(
            IPyDrawioExportManager, help="a drawio export service"
        )
    )
    manager = app.drawio_manager = IPyDrawioExportManager(parent=app, log=app.log)
    manager.initialize()
    add_handlers(app)
    app.log.warning(f"[ipydrawio] initialized: v{__version__}")
