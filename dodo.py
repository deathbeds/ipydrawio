"""automation for ipydrawio

> see https://pydoit.org/tutorial_1.html#incremental-computation

see what you can do

    doit list --status --all | sort

do basically everything to get ready for a release

    doit all

maybe before you push

    doit -n8 lint
"""
import shutil
import subprocess
import time
from hashlib import sha256

from doit.action import CmdAction
from doit.tools import PythonInteractiveAction, config_changed

import scripts.project as P

DOIT_CONFIG = dict(
    backend="sqlite3",
    verbosity=2,
    par_type="thread",
    default_tasks=["setup", "lint"],
)


def task_all():
    """do _everything_ (except start long-running servers)"""
    return dict(
        uptodate=[lambda: False],
        file_dep=[
            *P.OK_PYTEST.values(),
            P.OK_ATEST,
            P.OK_INTEGRITY,
            P.OK_PROVISION,
            P.SHA256SUMS,
        ],
        actions=[lambda: [print("nothing left to do"), True][1]],
    )


def task_dist():
    """create a minimum viable release product"""
    return dict(
        uptodate=[lambda: False],
        file_dep=[P.OK_INTEGRITY, P.SHA256SUMS, P.OK_LINT],
        actions=[lambda: print(P.SHA256SUMS.read_text())],
    )


def task_submodules():
    """ensure submodules are available"""
    subs = subprocess.check_output(["git", "submodule"]).decode("utf-8").splitlines()

    def _clean():
        """clean drawio, as it gets patched in-place"""
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
    """ perform general steps to get ready for development, testing, or releasing"""
    if not P.TESTING_IN_CI:
        yield dict(
            name="js",
            file_dep=[P.YARN_LOCK, P.PACKAGE, P.OK_SUBMODULES],
            actions=[
                [*P.JLPM, "--ignore-optional", "--prefer-offline"],
                [*P.LERNA, "bootstrap"],
            ],
            targets=[P.YARN_INTEGRITY],
        )

    for pkg, pkg_setup in P.PY_SETUP.items():
        # TODO: refactor
        ext_deps = [
            pkg_setup.parent
            / "src"
            / pkg.replace("-", "_")
            / "labextensions"
            / P.JS_PKG_DATA[ext]["name"]
            / "package.json"
            for ext, mod in P.JS_LABEXT_PY_HOST.items()
            if mod == pkg_setup.parent.name
        ]

        if P.TESTING_IN_CI:
            ci_af = {"wheel": P.PY_WHEEL[pkg], "sdist": P.PY_SDIST[pkg]}[P.CI_ARTIFACT]
            dist_af = P.DIST / ci_af.name

            yield _ok(
                dict(
                    name=f"py:{pkg}",
                    file_dep=[dist_af],
                    actions=[
                        [
                            "pip",
                            "install",
                            "-vv",
                            "--ignore-installed",
                            "--no-deps",
                            dist_af,
                        ],
                        ["python", "-m", "pip", "check"],
                    ],
                ),
                P.OK_PYSETUP[pkg],
            )
        else:
            yield _ok(
                dict(
                    name=f"py:{pkg}",
                    file_dep=[pkg_setup, P.PY_SETUP_CFG[pkg], *ext_deps],
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
                        CmdAction(
                            [
                                *P.LAB_EXT,
                                "develop",
                                "--overwrite",
                                ".",
                            ],
                            shell=False,
                            cwd=pkg_setup.parent,
                        ),
                        ["python", "-m", "pip", "check"],
                    ],
                ),
                P.OK_PYSETUP[pkg],
            )

    base_ext_args = [
        "jupyter",
        "serverextension",
        "enable",
        "--sys-prefix",
        "--py",
    ]
    for ext, ext_py in P.SERVER_EXT.items():
        enable_args = [*base_ext_args, ext_py.parent.name]

        if P.TESTING_IN_CI:
            enable_args = ["echo", "'(installed by pip)'"]

        yield _ok(
            dict(
                name=f"ext:{ext}",
                doc=f"ensure {ext} is a serverextension",
                file_dep=[ext_py, P.OK_PYSETUP[ext]],
                actions=[
                    enable_args,
                    ["jupyter", "serverextension", "list"],
                ],
            ),
            P.OK_SERVEREXT[ext],
        )


if not P.TESTING_IN_CI:

    def task_lint():
        """format all source files"""

        yield _ok(
            dict(
                name="isort",
                file_dep=[*P.ALL_PY],
                actions=[["isort", *P.ALL_PY]],
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
                actions=[
                    ["jlpm", "prettier", "--list-different", "--write", *P.ALL_PRETTIER]
                ],
            ),
            P.OK_PRETTIER,
        )
        yield _ok(
            dict(
                name="eslint",
                file_dep=[P.YARN_INTEGRITY, *P.ALL_TS, P.OK_PRETTIER, P.ESLINTRC],
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


if not P.TESTING_IN_CI:

    def task_build():
        yield _ok(
            dict(
                name="js:pre",
                file_dep=[P.YARN_INTEGRITY, P.IPDW_IGNORE, P.OK_SUBMODULES],
                actions=[[*P.LERNA, "run", "build:pre"]],
                targets=[P.IPDW_APP],
            ),
            P.OK_JS_BUILD_PRE,
        )

        yield _ok(
            dict(
                name="js",
                file_dep=[P.YARN_INTEGRITY, P.OK_JS_BUILD_PRE, *P.ALL_TS, *P.ALL_CSS],
                actions=[[*P.LERNA, "run", "build", "--stream"]],
                targets=sorted(P.JS_TSBUILDINFO.values()),
            ),
            P.OK_JS_BUILD,
        )

        for pkg, (file_dep, targets) in P.JS_PKG_PACK.items():
            yield dict(
                name=f"pack:{pkg}",
                file_dep=file_dep,
                actions=[
                    CmdAction(
                        [P.NPM, "pack", "."], cwd=str(targets[0].parent), shell=False
                    )
                ],
                targets=targets,
            )
            pkg_data = P.JS_PKG_DATA[pkg]

            if "jupyterlab" not in pkg_data:
                continue

            host = P.JS_LABEXT_PY_HOST[pkg]
            host_mod = host.replace("-", "_")
            host_ext = P.PY_PACKAGES / host / "src" / host_mod / "labextensions"

            yield _ok(
                dict(
                    name=f"ext:build:{pkg}",
                    actions=[
                        CmdAction(
                            [*P.LAB_EXT, "build", "."],
                            shell=False,
                            cwd=P.JS_PKG_JSON[pkg].parent,
                        )
                    ],
                    file_dep=targets,
                    targets=[host_ext / f"""{pkg_data["name"]}/package.json"""],
                ),
                P.OK_EXT_BUILD[pkg],
            )

        for py_pkg, py_setup in P.PY_SETUP.items():
            py_mod = py_setup.parent.name.replace("-", "_")
            ext_deps = [
                py_setup.parent
                / "src"
                / py_mod
                / "labextensions"
                / P.JS_PKG_DATA[ext]["name"]
                / "package.json"
                for ext, mod in P.JS_LABEXT_PY_HOST.items()
                if mod == py_setup.parent.name
            ]
            file_dep = sorted(
                set(
                    [
                        *ext_deps,
                        *P.PY_SRC[py_pkg],
                        P.OK_SUBMODULES,
                        py_setup,
                        py_setup.parent / "setup.cfg",
                        py_setup.parent / "MANIFEST.in",
                    ]
                )
            )
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

        def _make_hashfile():
            # mimic sha256sum CLI
            if P.SHA256SUMS.exists():
                P.SHA256SUMS.unlink()

            if not P.DIST.exists():
                P.DIST.mkdir(parents=True)

            [shutil.copy2(p, P.DIST / p.name) for p in P.HASH_DEPS]

            lines = []

            for p in P.HASH_DEPS:
                lines += ["  ".join([sha256(p.read_bytes()).hexdigest(), p.name])]

            output = "\n".join(lines)
            print(output)
            P.SHA256SUMS.write_text(output)

        yield dict(
            name="hash",
            file_dep=[*P.HASH_DEPS],
            targets=[P.SHA256SUMS, *[P.DIST / d.name for d in P.HASH_DEPS]],
            actions=[_make_hashfile],
        )


if not P.TESTING_IN_CI:

    def task_lab():
        """run JupyterLab "normally" (not watching sources)"""

        def lab():
            proc = subprocess.Popen(P.CMD_LAB, stdin=subprocess.PIPE)

            try:
                proc.wait()
            except KeyboardInterrupt:
                print(
                    "attempting to stop lab, you may want to check your process monitor"
                )
                proc.terminate()
                proc.communicate(b"y\n")

            proc.wait()

        return dict(
            uptodate=[lambda: False],
            file_dep=[*P.OK_SERVEREXT.values()],
            actions=[PythonInteractiveAction(lab)],
        )


def _make_lab(watch=False):
    def _lab():
        if watch:
            print(">>> Starting typescript watcher...", flush=True)
            ts = subprocess.Popen([*P.LERNA, "run", "watch"])

            ext_watchers = [
                subprocess.Popen([*P.LAB_EXT, "watch", "."], cwd=str(p.parent))
                for p in P.JS_PKG_JSON_LABEXT.values()
            ]

            print(">>> Waiting a bit to JupyterLab...", flush=True)
            time.sleep(3)
        print(">>> Starting JupyterLab...", flush=True)
        lab = subprocess.Popen(
            P.CMD_LAB,
            stdin=subprocess.PIPE,
        )

        try:
            print(">>> Waiting for JupyterLab to exit (Ctrl+C)...", flush=True)
            lab.wait()
        except KeyboardInterrupt:
            print(
                f""">>> {"Watch" if watch else "Run"} canceled by user!""",
                flush=True,
            )
        finally:
            print(">>> Stopping watchers...", flush=True)
            if watch:
                [x.terminate() for x in ext_watchers]
                ts.terminate()
            lab.terminate()
            lab.communicate(b"y\n")
            if watch:
                ts.wait()
                lab.wait()
                [x.wait() for x in ext_watchers]
                print(
                    ">>> Stopped watchers! maybe check process monitor...",
                    flush=True,
                )

        return True

    return _lab


if not P.TESTING_IN_CI:

    def task_watch():
        """watch labextensions for changes, rebuilding"""

        return dict(
            uptodate=[lambda: False],
            file_dep=[*P.OK_SERVEREXT.values(), *P.OK_PYSETUP.values()],
            actions=[
                P.CMD_LIST_EXTENSIONS,
                PythonInteractiveAction(_make_lab(watch=True)),
            ],
        )


def task_provision():
    """ensure the ipydrawio-export server has been provisioned with npm (ick)"""
    return _ok(
        dict(
            file_dep=[*P.OK_SERVEREXT.values()],
            actions=[
                ["jupyter", "ipydrawio-export", "--version"],
                ["jupyter", "ipydrawio-export", "provision"],
            ],
        ),
        P.OK_PROVISION,
    )


def _pytest(setup_py):
    def _test():
        subprocess.check_call(
            [*P.PYM, "pytest", *P.PYTEST_ARGS], shell=False, cwd=str(setup_py.parent)
        )

    return _test


def task_test():
    if not P.TESTING_IN_CI:
        yield _ok(
            dict(
                name="integrity",
                file_dep=[
                    P.SCRIPTS / "integrity.py",
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
                uptodate=[config_changed(dict(PYTEST_ARGS=P.PYTEST_ARGS))],
                file_dep=[
                    *P.PY_SRC[pkg],
                    *P.PY_TEST_DEP.get(pkg, []),
                    P.OK_PROVISION,
                    P.OK_PYSETUP[pkg],
                ],
                actions=[PythonInteractiveAction(_pytest(setup))],
            ),
            P.OK_PYTEST[pkg],
        )

    file_dep = [
        *P.ALL_ROBOT,
        P.OK_PROVISION,
        P.SCRIPTS / "atest.py",
    ]

    if not P.TESTING_IN_CI:
        file_dep += [P.OK_ROBOT_DRYRUN]

    yield _ok(
        dict(
            name="robot",
            uptodate=[config_changed(dict(ATEST_ARGS=P.ATEST_ARGS))],
            file_dep=file_dep,
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
