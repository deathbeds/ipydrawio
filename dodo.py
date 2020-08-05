import subprocess

from doit.tools import PythonInteractiveAction

import scripts.project as P

DOIT_CONFIG = {"backend": "sqlite3", "verbosity": 2, "par_type": "thread"}


def task_setup():
    yield dict(
        name="js",
        file_dep=[P.YARN_LOCK],
        actions=[
            [*P.JLPM, "--ignore-optional", "--prefer-offline"],
            [*P.JLPM, "lerna", "bootstrap"],
        ],
        targets=[P.YARN_INTEGRITY],
    )


def task_lint():
    """ format all source files
    """

    yield _ok(
        dict(
            name="isort", file_dep=[*P.ALL_PY], actions=[["isort", "-rc", *P.ALL_PY]],
        ),
        P.OK_ISORT,
    )
    yield _ok(
        dict(
            name="black",
            file_dep=[*P.ALL_PY, P.OK_ISORT],
            actions=[["black", "--quiet", *P.ALL_PY]],
        ),
        P.OK_BLACK,
    )
    yield _ok(
        dict(
            name="flake8",
            file_dep=[*P.ALL_PY, P.OK_BLACK],
            actions=[["flake8", *P.ALL_PY]],
        ),
        P.OK_FLAKE8,
    )
    yield _ok(
        dict(
            name="pyflakes",
            file_dep=[*P.ALL_PY, P.OK_BLACK],
            actions=[["pyflakes", *P.ALL_PY]],
        ),
        P.OK_PYFLAKES,
    )
    yield _ok(
        dict(
            name="prettier",
            file_dep=[P.YARN_INTEGRITY, *P.ALL_PRETTIER],
            actions=[["jlpm", "prettier", "--write", *P.ALL_PRETTIER]],
        ),
        P.OK_PRETTIER,
    )
    yield _ok(
        dict(
            name="eslint",
            file_dep=[P.YARN_INTEGRITY, *P.ALL_PRETTIER, P.OK_PRETTIER],
            actions=[["jlpm", "eslint"]],
        ),
        P.OK_ESLINT,
    )
    yield _ok(
        dict(
            name="all",
            actions=[_echo_ok("all ok")],
            file_dep=[
                P.OK_BLACK,
                P.OK_FLAKE8,
                P.OK_ISORT,
                P.OK_PRETTIER,
                P.OK_PYFLAKES,
            ],
        ),
        P.OK_LINT,
    )


def task_build():
    yield dict(
        name="js",
        file_dep=[P.YARN_INTEGRITY],
        actions=[[*P.JLPM, "lerna", "run", "build"]],
    )


def task_lab():
    """ run JupyterLab "normally" (not watching sources)
    """

    def lab():
        proc = subprocess.Popen(
            ["jupyter", "lab", "--no-browser", "--debug"], stdin=subprocess.PIPE
        )

        try:
            proc.wait()
        except KeyboardInterrupt:
            print("attempting to stop lab, you may want to check your process monitor")
            proc.terminate()
            proc.communicate(b"y\n")

        proc.wait()

    return dict(
        uptodate=[lambda: False],
        file_dep=[P.LAB_INDEX],
        actions=[PythonInteractiveAction(lab)],
    )


def _echo_ok(msg):
    def _echo():
        print(msg, flush=True)
        return True

    return _echo


def _ok(task, ok):
    task.setdefault("targets", []).append(ok)
    task["actions"] = [
        lambda: [ok.exists() and ok.unlink(), True][-1],
        *task["actions"],
        lambda: [ok.parent.mkdir(exist_ok=True), ok.write_text("ok"), True][-1],
    ]
    return task
