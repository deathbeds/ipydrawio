"""
CLI for jupyter-drawio-export

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

from traitlets.config import Application

from ._version import __version__
from .manager import DrawioExportManager


class BaseApp(Application):
    version = __version__

    @property
    def description(self):
        return self.__doc__.splitlines()[0].strip()


class ProvisionApp(BaseApp):
    """ pre-provision drawio export tools
    """

    def start(self):
        manager = self.drawio_manager = DrawioExportManager(parent=self, log=self.log)
        manager.initialize()
        manager.provision(force=True)


class DrawioExportApp(BaseApp):
    """ drawio export tools
    """

    name = "drawio-export"
    subcommands = dict(provision=(ProvisionApp, ProvisionApp.__doc__.splitlines()[0]),)


main = launch_instance = DrawioExportApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()
