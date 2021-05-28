"""automation for ipydrawio

> see https://pydoit.org/tutorial_1.html#incremental-computation

see what you can do

    doit list --status --all | sort

do basically everything to get ready for a release

    doit all

maybe before you push

    doit -n8 lint
"""

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

import pprint
import shutil
import subprocess
import time
from hashlib import sha256

import doit
from doit.action import CmdAction
from doit.tools import PythonInteractiveAction, config_changed

import scripts.project as P

print_ = pprint.pprint
console = None

try:
    import rich.console
    import rich.markdown

    console = rich.console.Console()
    print_ = console.print

except ImportError:
    pass


DOIT_CONFIG = dict(
    backend="sqlite3",
    verbosity=2,
    par_type="thread",
    default_tasks=["setup"],
)


def task_all():
    """do _everything_ (except start long-running servers)"""
    return dict(
        uptodate=[lambda: False],
        task_dep=["check"],
        file_dep=[
            *[P.OK_CONDA_TEST / f"{name}.ok" for name in P.CONDA_PKGS],
            *P.OK_PYTEST.values(),
            P.DOCS_BUILDINFO,
            P.OK_ATEST,
            P.OK_INTEGRITY,
            P.OK_LINK_CHECK,
            P.OK_PROVISION,
            P.SHA256SUMS,
        ],
        actions=[(_show, ["nothing left to do"], {"shasums": P.SHA256SUMS.read_text})],
    )


def task_fetch():
    """fetch local copies of key configuration documentation"""
    for path, url in P.DIA_URLS.items():
        yield P.fetch_one(url, path)


def task_dist():
    """create a minimum viable release product"""
    return dict(
        uptodate=[lambda: False],
        file_dep=[P.OK_INTEGRITY, P.SHA256SUMS, P.OK_LINT],
        actions=[lambda: print(P.SHA256SUMS.read_text())],
    )


def task_env():
    """sync environments"""
    for env, inherits in P.ENV_INHERITS.items():
        yield dict(
            name=f"""{env.parent.name}:{':'.join([inh.parent.name for inh in inherits])}""",
            file_dep=[*inherits, P.YARN_INTEGRITY],
            actions=[(P.patch_one_env, [inh, env]) for inh in inherits]
            + [["jlpm", "prettier", "--list-different", "--write", env]],
            targets=[env],
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
    """perform general steps to get ready for development, testing, or releasing"""
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
            (
                P.JS_PKG_JSON[ext].parent
                / P.JS_PKG_DATA[ext]["jupyterlab"]["outputDir"]
            ).resolve()
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
                            *P.PIP,
                            "install",
                            "-vv",
                            "--ignore-installed",
                            "--no-deps",
                            dist_af,
                        ]
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
                                *P.PIP,
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
                                "--debug",
                                "--overwrite",
                                ".",
                            ],
                            shell=False,
                            cwd=pkg_setup.parent,
                        ),
                    ],
                ),
                P.OK_PYSETUP[pkg],
            )

    yield _ok(
        dict(
            name="pip:check",
            file_dep=[*P.OK_PYSETUP.values()],
            actions=[[*P.PIP, "check"]],
        ),
        P.OK_PIP_CHECK,
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
                file_dep=[ext_py, P.OK_PIP_CHECK],
                actions=[
                    enable_args,
                    ["jupyter", "serverextension", "list"],
                ],
            ),
            P.OK_SERVEREXT[ext],
        )


def task_lint():
    """format all source files"""

    if P.TESTING_IN_CI:
        return

    yield _ok(
        dict(
            name="isort",
            file_dep=[*P.ALL_PY, P.SETUP_CFG],
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
            file_dep=[*P.ALL_PY, P.OK_BLACK, P.SETUP_CFG],
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
                [
                    "jlpm",
                    "prettier",
                    "--list-different",
                    "--write",
                    *sorted(p.relative_to(P.ROOT) for p in P.ALL_PRETTIER),
                ]
            ],
        ),
        P.OK_PRETTIER,
    )
    yield _ok(
        dict(
            name="eslint",
            file_dep=[
                P.YARN_INTEGRITY,
                *P.ALL_TS,
                P.OK_PRETTIER,
                P.ESLINTRC,
                P.TSCONFIGBASE,
            ],
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
    """build intermediates and release artifacts"""
    if P.TESTING_IN_CI:
        return

    yield _ok(
        dict(
            name="js:pre",
            file_dep=[
                P.YARN_INTEGRITY,
                P.IPDW_IGNORE,
                P.OK_SUBMODULES,
                *sum(P.JS_PY_SCRIPTS.values(), []),
                *sum(P.JS_SCHEMAS.values(), []),
            ],
            actions=[[*P.LERNA, "run", "build:pre", "--stream"]],
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

    yield dict(
        name="readme:ipydrawio",
        file_dep=[P.README],
        targets=[P.IPD / "README.md"],
        actions=[
            lambda: [(P.IPD / "README.md").write_text(P.README.read_text()), None][-1]
        ],
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
        pkg_data = P.JS_PKG_DATA[pkg]

        if "jupyterlab" not in pkg_data:
            continue

        out_dir = (
            P.JS_PKG_JSON[pkg].parent / pkg_data["jupyterlab"]["outputDir"]
        ).resolve()

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
                targets=[out_dir / "package.json"],
            ),
            P.OK_EXT_BUILD[pkg],
        )

    for py_pkg, py_setup in P.PY_SETUP.items():
        ext_deps = [
            (
                P.JS_PKG_JSON[ext].parent
                / P.JS_PKG_DATA[ext]["jupyterlab"]["outputDir"]
            ).resolve()
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
                    py_setup.parent / "README.md",
                    py_setup.parent / "LICENSE.txt",
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


def task_conda():
    """test building with conda-build"""
    args = [
        "conda",
        P.CONDA_BUILDERER,
        "-c",
        "conda-forge",
    ]

    yield dict(
        name="build",
        file_dep=[
            P.RECIPE,
            *[P.DIST / p.name for p in P.PY_SDIST.values()],
        ],
        actions=[
            [
                *args,
                "--no-test",
                "--output-folder",
                P.CONDA_BLD,
                P.RECIPE.parent,
            ]
        ],
        targets=[*P.CONDA_PKGS.values()],
    )

    for name, pkg in P.CONDA_PKGS.items():
        yield _ok(
            dict(
                name=f"test:{name}",
                file_dep=[pkg],
                actions=[[*args, "--test", pkg]],
            ),
            P.OK_CONDA_TEST / f"{name}.ok",
        )


def task_lab():
    """run JupyterLab "normally" (not watching sources)"""
    if P.TESTING_IN_CI:
        return

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


def task_watch():
    """watch things"""
    if P.TESTING_IN_CI:
        return

    yield dict(
        name="lab",
        doc="watch labextensions for changes, rebuilding",
        uptodate=[lambda: False],
        file_dep=[*P.OK_SERVEREXT.values(), P.OK_PIP_CHECK],
        actions=[
            P.CMD_LIST_EXTENSIONS,
            PythonInteractiveAction(_make_lab(watch=True)),
        ],
    )

    yield dict(
        name="docs",
        doc="watch docs for changes, rebuilding",
        uptodate=[lambda: False],
        file_dep=[P.DOCS_BUILDINFO, P.OK_PIP_CHECK],
        actions=[["sphinx-autobuild", *P.SPHINX_ARGS, "-j8", P.DOCS, P.DOCS_BUILD]],
    )


def task_docs():
    """build the docs"""
    if P.TESTING_IN_CI:
        return

    if shutil.which("convert"):
        yield dict(
            name="favicon",
            doc="regenerate the favicon",
            file_dep=[P.DOCS_FAVICON_SVG],
            actions=[
                [
                    "convert",
                    "-density",
                    "256x256",
                    "-background",
                    "transparent",
                    P.DOCS_FAVICON_SVG,
                    "-define",
                    "icon:auto-resize",
                    "-colors",
                    "256",
                    P.DOCS_FAVICON_ICO,
                ]
            ],
            targets=[P.DOCS_FAVICON_ICO],
        )

    yield dict(
        name="typedoc:ensure",
        file_dep=[*P.JS_PKG_JSON.values()],
        actions=[P.typedoc_conf],
        targets=[P.TYPEDOC_JSON, P.TSCONFIG_TYPEDOC],
    )

    yield dict(
        name="typedoc:build",
        doc="build the TS API documentation with typedoc",
        file_dep=[*P.JS_TSBUILDINFO.values(), *P.TYPEDOC_CONF, P.YARN_INTEGRITY],
        actions=[["jlpm", "typedoc", "--options", P.TYPEDOC_JSON]],
        targets=[P.DOCS_RAW_TYPEDOC_README],
    )

    yield dict(
        name="typedoc:mystify",
        doc="transform raw typedoc into myst markdown",
        file_dep=[P.DOCS_RAW_TYPEDOC_README],
        targets=[P.DOCS_TS_MYST_INDEX, *P.DOCS_TS_MODULES],
        actions=[
            P.mystify,
            [
                "jlpm",
                "prettier",
                "--list-different",
                "--write",
                P.DOCS_TS_MYST_INDEX.parent,
            ],
        ],
    )

    yield dict(
        name="sphinx",
        doc="build the documentation site with sphinx",
        file_dep=[P.DOCS_CONF, P.DOCS_FAVICON_ICO, P.OK_PIP_CHECK, *P.DOCS_SRC],
        actions=[
            ["sphinx-build", *P.SPHINX_ARGS, "-j8", "-b", "html", P.DOCS, P.DOCS_BUILD]
        ],
        targets=[P.DOCS_BUILDINFO],
    )


@doit.create_after("docs")
def task_check():
    """check built artifacts"""
    file_dep = [*P.DOCS_BUILD.rglob("*.html")]
    yield _ok(
        dict(
            name="links",
            file_dep=[*file_dep, P.DOCS_BUILDINFO],
            actions=[
                [
                    "pytest-check-links",
                    "--check-anchors",
                    "--check-links-ignore",
                    "^https?://",
                    *[p for p in file_dep if p.name != "schema.html"],
                ]
            ],
        ),
        P.OK_LINK_CHECK,
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
    """run tests"""
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
                    P.PY_SETUP_CFG[pkg],
                    *P.PY_TEST_DEP.get(pkg, []),
                    P.OK_PROVISION,
                    P.OK_PIP_CHECK,
                ],
                actions=[PythonInteractiveAction(_pytest(setup))],
            ),
            P.OK_PYTEST[pkg],
        )

    file_dep = [
        *P.ALL_ROBOT,
        P.OK_PROVISION,
        *sum(P.PY_SRC.values(), []),
        *sum(P.JS_TSSRC.values(), []),
        P.SCRIPTS / "atest.py",
    ]

    if not P.TESTING_IN_CI:
        file_dep += [P.OK_ROBOT_DRYRUN, *P.OK_SERVEREXT.values()]

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


def _show(*args, **kwargs):
    for arg in args:
        print_(arg()) if callable(arg) else print_(arg)
    for kw, kwarg in kwargs.items():
        print_(rich.markdown.Markdown(f"# {kw}") if console else kw)
        print_(kwarg()) if callable(kwarg) else print_(kwarg)
