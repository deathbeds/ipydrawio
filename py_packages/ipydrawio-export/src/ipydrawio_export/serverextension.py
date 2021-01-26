"""
add drawio support to the running jupyter notebook application

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

import traitlets

from .handlers import add_handlers
from .manager import DrawioExportManager


def load_jupyter_server_extension(nbapp):
    """create a DrawioExportManager and add handlers"""
    nbapp.add_traits(drawio_manager=traitlets.Instance(DrawioExportManager))
    manager = nbapp.drawio_manager = DrawioExportManager(parent=nbapp, log=nbapp.log)
    manager.initialize()
    add_handlers(nbapp)
    nbapp.log.warning("drawio initialized %s", manager)
