import shutil
import subprocess

from doit.action import CmdAction
from doit.tools import PythonInteractiveAction, config_changed

import scripts.project as P

DOIT_CONFIG = dict(
    backend="sqlite3",
    verbosity=2,
    par_type="thread",
    default_tasks=["setup", "lab_build:extensions"],
)


def task_submodules():
    """ ensure submodules are available
    """
    subs = subprocess.check_output(["git", "submodule"]).decode("utf-8").splitlines()

    def _clean():
        """ clean drawio, as it gets patched in-place
        """
        if any([x.startswith("-") for x in subs]) and P.DRAWIO.exists():
            shutil.rmtree(P.DRAWIO)

    return _ok(
        dict(
            uptodate=[config_changed({"subs": subs})],
            actions=[_clean, ["git", "submodule", "update", "--init", "--recursive"]],
        ),
        P.OK_SUBMODULES,
    )


def task_setup():
    yield dict(
        name="js",
        file_dep=[P.YARN_LOCK, P.PACKAGE, P.OK_SUBMODULES],
        actions=[
            [*P.JLPM, "--ignore-optional", "--prefer-offline"],
            [*P.JLPM, "lerna", "bootstrap"],
        ],
        targets=[P.YARN_INTEGRITY],
    )

    for pkg, pkg_setup in P.PY_SETUP.items():
        yield _ok(
            dict(
                name=f"py:{pkg}",
                file_dep=[pkg_setup, P.PY_SETUP_CFG[pkg]],
                actions=[
                    CmdAction(
                        [
                            "python",
                            "-m",
                            "pip",
                            "install",
                            "-e",
                            ".",
                            "--no-deps",
                            "-vv",
                        ],
                        shell=False,
                        cwd=pkg_setup.parent,
                    ),
                    ["python", "-m", "pip", "check"],
                ],
            ),
            P.OK_PYSETUP[pkg],
        )

    for ext, ext_py in P.SERVER_EXT.items():
        yield _ok(
            dict(
                name=f"ext:{ext}",
                file_dep=[ext_py, P.OK_PYSETUP[ext]],
                actions=[
                    [
                        "jupyter",
                        "serverextension",
                        "enable",
                        "--py",
                        "jupyter_drawio_export",
                        "--sys-prefix",
                    ],
                    ["jupyter", "serverextension", "list"],
                ],
            ),
            P.OK_SERVEREXT[ext],
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
            file_dep=[P.YARN_INTEGRITY, *P.ALL_TS, P.OK_PRETTIER],
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

    yield _ok(
        dict(
            name="robot:tidy",
            file_dep=P.ALL_ROBOT,
            actions=[[*P.PYM, "robot.tidy", "--inplace", *P.ALL_ROBOT]],
        ),
        P.OK_ROBOTIDY,
    )

    yield _ok(
        dict(
            name="robot:lint",
            file_dep=[*P.ALL_ROBOT, P.OK_ROBOTIDY],
            actions=[["rflint", *P.RFLINT_OPTS, *P.ALL_ROBOT]],
        ),
        P.OK_RFLINT,
    )

    yield _ok(
        dict(
            name="robot:dryrun",
            file_dep=[*P.ALL_ROBOT, P.OK_RFLINT],
            actions=[[*P.PYM, "scripts.atest", "--dryrun"]],
        ),
        P.OK_ROBOT_DRYRUN,
    )


def task_build():
    yield _ok(
        dict(
            name="js:pre",
            file_dep=[P.YARN_INTEGRITY, P.JDW_IGNORE, P.OK_SUBMODULES],
            actions=[[*P.JLPM, "lerna", "run", "build:pre"]],
            targets=[P.JDW_APP],
        ),
        P.OK_JS_BUILD_PRE,
    )

    yield _ok(
        dict(
            name="js",
            file_dep=[P.YARN_INTEGRITY, P.OK_JS_BUILD_PRE, *P.ALL_TS, *P.ALL_CSS],
            actions=[[*P.JLPM, "lerna", "run", "build"]],
            targets=sorted(P.JS_TSBUILDINFO.values()),
        ),
        P.OK_JS_BUILD,
    )

    for pkg, (file_dep, targets) in P.JS_PKG_PACK.items():
        yield dict(
            name=f"pack:{pkg}",
            file_dep=file_dep,
            actions=[
                CmdAction([P.NPM, "pack", "."], cwd=str(targets[0].parent), shell=False)
            ],
            targets=targets,
        )

    for py_pkg, py_setup in P.PY_SETUP.items():
        file_dep = [py_setup, *P.PY_SRC[py_pkg], P.OK_SUBMODULES]
        yield dict(
            name=f"sdist:{py_pkg}",
            file_dep=file_dep,
            actions=[
                CmdAction(
                    ["python", "setup.py", "sdist"],
                    shell=False,
                    cwd=str(py_setup.parent),
                ),
            ],
            targets=[P.PY_SDIST[py_pkg]],
        )
        yield dict(
            name=f"whl:{py_pkg}",
            file_dep=file_dep,
            actions=[
                CmdAction(
                    ["python", "setup.py", "bdist_wheel"],
                    shell=False,
                    cwd=str(py_setup.parent),
                ),
            ],
            targets=[P.PY_WHEEL[py_pkg]],
        )


def task_lab_build():
    """ do a "production" build of lab
    """

    file_dep = sorted(P.JS_TARBALL.values())

    build_args = ["--dev-build=False", "--minimize=True"]
    if P.WIN:
        build_args = []

    yield dict(
        name="extensions",
        file_dep=[*file_dep, P.OVERRIDES],
        uptodate=[config_changed({"exts": P.EXTENSIONS})],
        actions=[
            P.CMD_DISABLE_EXTENSIONS,
            P.CMD_INSTALL_ALL_EXTENSIONS,
            P.CMD_LIST_EXTENSIONS,
            P._override_lab,
            [*P.CMD_BUILD, *build_args],
            P.CMD_LIST_EXTENSIONS,
        ],
        targets=[P.LAB_INDEX, P.LAB_OVERRIDES, P.LAB_LOCK],
    )


def task_lab():
    """ run JupyterLab "normally" (not watching sources)
    """

    def lab():
        proc = subprocess.Popen(P.CMD_LAB, stdin=subprocess.PIPE)

        try:
            proc.wait()
        except KeyboardInterrupt:
            print("attempting to stop lab, you may want to check your process monitor")
            proc.terminate()
            proc.communicate(b"y\n")

        proc.wait()

    return dict(
        uptodate=[lambda: False],
        file_dep=[P.LAB_INDEX, *P.OK_SERVEREXT.values()],
        actions=[PythonInteractiveAction(lab)],
    )


def task_watch():
    def watch():
        shutil.rmtree(P.LAB_STATIC, ignore_errors=True)
        subprocess.check_call(["jupyter", "lab", "build"])

        for sub_ns in (P.LAB_STAGING / "node_modules" / f"@{P.JS_NS}").glob(
            f"*/node_modules/@{P.JS_NS}"
        ):
            print(f"Deleting {sub_ns.relative_to(P.LAB_STAGING)}", flush=True)
            shutil.rmtree(sub_ns)
        else:
            print(f"Nothing deleted in {P.LAB_STAGING}!", flush=True)

        jlpm_proc = subprocess.Popen(
            ["jlpm", "lerna", "run", "--parallel", "--stream", "watch"]
        )

        build_proc = subprocess.Popen(["jlpm", "watch"], cwd=P.LAB_STAGING)

        lab_proc = subprocess.Popen(P.CMD_LAB, stdin=subprocess.PIPE)

        try:
            lab_proc.wait()
        except KeyboardInterrupt:
            print("attempting to stop lab, you may want to check your process monitor")
            lab_proc.terminate()
            lab_proc.communicate(b"y\n")
        finally:
            jlpm_proc.terminate()
            build_proc.terminate()

        lab_proc.wait()
        jlpm_proc.wait()
        build_proc.wait()

    return dict(
        uptodate=[lambda: False],
        file_dep=[*P.JS_TARBALL.values(), *P.OK_SERVEREXT.values()],
        actions=[
            P.CMD_LIST_EXTENSIONS,
            P.CMD_LINK_EXTENSIONS,
            P.CMD_LIST_EXTENSIONS,
            P.CMD_INSTALL_EXTENSIONS,
            P.CMD_DISABLE_EXTENSIONS,
            P._override_lab,
            P.CMD_LIST_EXTENSIONS,
            PythonInteractiveAction(watch),
        ],
    )


def task_provision():
    return _ok(
        dict(
            file_dep=[*P.OK_SERVEREXT.values()],
            actions=[
                ["jupyter", "drawio-export", "--version"],
                ["jupyter", "drawio-export", "provision"],
            ],
        ),
        P.OK_PROVISION,
    )


def task_all():
    return dict(
        file_dep=[P.OK_INTEGRITY, P.OK_PROVISION, P.OK_ATEST, *P.OK_PYTEST.values()],
        actions=[lambda: [print("nothing left to do"), True][1]],
    )


def _pytest(setup_py):
    def _test():
        subprocess.check_call([*P.PYM, "pytest"], shell=False, cwd=str(setup_py.parent))

    return _test


def task_test():
    yield _ok(
        dict(
            name="integrity",
            file_dep=[
                P.SCRIPTS / "integrity.py",
                P.LAB_INDEX,
                P.OK_LINT,
                *[*P.OK_SERVEREXT.values()],
                *[*P.PY_WHEEL.values()],
                *[*P.PY_SDIST.values()],
            ],
            actions=[
                ["python", "-m", "pytest", "--pyargs", "scripts.integrity", "-vv"]
            ],
        ),
        P.OK_INTEGRITY,
    )

    for pkg, setup in P.PY_SETUP.items():
        yield _ok(
            dict(
                name=f"pytest:{pkg}",
                file_dep=[*P.PY_SRC[pkg]],
                actions=[PythonInteractiveAction(_pytest(setup))],
            ),
            P.OK_PYTEST[pkg],
        )

    yield _ok(
        dict(
            name="robot",
            file_dep=[
                *P.ALL_ROBOT,
                P.LAB_INDEX,
                P.LAB_OVERRIDES,
                P.OK_PROVISION,
                P.OK_ROBOT_DRYRUN,
                P.SCRIPTS / "atest.py",
            ],
            actions=[["python", "-m", "scripts.atest"]],
        ),
        P.OK_ATEST,
    )


# utilities
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
