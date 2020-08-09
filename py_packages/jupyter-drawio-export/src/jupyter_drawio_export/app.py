from traitlets.config import Application

from .manager import DrawioExportManager


class DrawioExportApp(Application):
    description = """drawio export tools"""

    def start(self):
        manager = self.drawio_manager = DrawioExportManager(parent=self, log=self.log)
        manager.initialize()
        manager.provision(force=True)


main = launch_instance = DrawioExportApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()
