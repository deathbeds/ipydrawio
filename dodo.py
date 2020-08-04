import os
import shutil
import subprocess

import scripts.project as P
from doit.tools import PythonInteractiveAction, config_changed, result_dep

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread"
}


def task_setup():
    yield dict(
        name="js",
        file_dep=[P.YARN_LOCK],
        actions=[
            [*P.JLPM, "--ignore-optional", "--prefer-offline"],
            [*P.JLPM, "lerna", "bootstrap"]
        ],
        targets=[P.YARN_INTEGRITY]
    )

def task_build():
    yield dict(
        name="js",
        file_dep=[P.YARN_INTEGRITY],
        actions=[
            [*P.JLPM, "lerna", "run", "build"]
        ]
    )
