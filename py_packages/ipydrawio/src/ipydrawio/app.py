"""CLI for ipydrawio"""

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

from pathlib import Path

import traitlets as T
from jupyter_core.application import base_flags
from traitlets.config import Application

from ._version import __version__
from .utils import clean_drawio_file


class BaseApp(Application):
    version = __version__

    @property
    def description(self):  # pragma: no cover
        return self.__doc__.splitlines()[0].strip()


class CleanApp(BaseApp):
    """clean drawio files"""

    dio_files = T.Tuple()

    flags = dict(**base_flags)

    def parse_command_line(self, argv=None):
        super().parse_command_line(argv)
        self.dio_files = [Path(p).resolve() for p in self.extra_args]

    def start(self):
        for path in self.dio_files:
            clean_drawio_file(path)


class IPyDrawioApp(BaseApp):
    """ipydrawio utilities"""

    name = "ipydrawio"
    subcommands = dict(
        clean=(CleanApp, CleanApp.__doc__.splitlines()[0]),
    )


main = launch_instance = IPyDrawioApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()
