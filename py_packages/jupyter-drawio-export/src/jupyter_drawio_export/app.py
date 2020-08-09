""" CLI for drawio-export
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
