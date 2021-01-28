""" important project paths

    this should not import anything not in py36+ stdlib, or any local paths
"""
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

# platform
PLATFORM = os.environ.get("FAKE_PLATFORM", platform.system())
WIN = PLATFORM == "Windows"
OSX = PLATFORM == "Darwin"
UNIX = not WIN
PREFIX = Path(sys.prefix)

BUILDING_IN_CI = bool(json.loads(os.environ.get("BUILDING_IN_CI", "0")))
TESTING_IN_CI = bool(json.loads(os.environ.get("TESTING_IN_CI", "0")))
CI_ARTIFACT = os.environ.get("CI_ARTIFACT", "wheel")

# test arg pass-throughs
ATEST_ARGS = json.loads(os.environ.get("ATEST_ARGS", "[]"))
ATEST_RETRIES = int(os.environ.get("ATEST_RETRIES") or "0")
PYTEST_ARGS = json.loads(os.environ.get("PYTEST_ARGS", "[]"))
ATEST_PROCS = int(os.environ.get("ATEST_PROCS", "4"))

# find root
SCRIPTS = Path(__file__).parent.resolve()
ROOT = SCRIPTS.parent
BINDER = ROOT / "binder"
PY_MAJOR = "".join(map(str, sys.version_info[:2]))

# top-level stuff
NODE_MODULES = ROOT / "node_modules"
PACKAGE = ROOT / "package.json"
PACKAGES = ROOT / "packages"
YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"
YARN_LOCK = ROOT / "yarn.lock"
OVERRIDES = ROOT / "overrides.json"
CI = ROOT / ".github"
DODO = ROOT / "dodo.py"
BUILD = ROOT / "build"
DIST = ROOT / "dist"

# tools
PY = ["python"]
PYM = [*PY, "-m"]
PIP = [*PYM, "pip"]

NPM = (
    shutil.which("npm")
    or shutil.which("npm.cmd")
    or shutil.which("npm.exe")
    or shutil.which("npm.bat")
)
JLPM = ["jlpm"]
LERNA = [*JLPM, "lerna"]
JLPM_INSTALL = [*JLPM, "--ignore-optional", "--prefer-offline"]
LAB_EXT = ["jupyter", "labextension"]
LAB = ["jupyter", "lab"]
PRETTIER = [str(NODE_MODULES / ".bin" / "prettier")]

# tests
EXAMPLES = ROOT / "notebooks"
EXAMPLE_IPYNB = [
    p for p in EXAMPLES.rglob("*.ipynb") if ".ipynb_checkpoints" not in str(p)
]
DIST_NBHTML = DIST / "nbsmoke"
ATEST = ROOT / "atest"
ATEST_OUT = ATEST / "output"
ATEST_OUT_XML = "output.xml"

# js packages
JS_NS = "deathbeds"
IPYDIO = PACKAGES / "ipydrawio"

# so many js packages
JS_PKG_JSON = {p.parent.name: p for p in PACKAGES.glob("*/package.json")}

JS_PKG_DATA = {
    k: json.loads(v.read_text(encoding="utf-8")) for k, v in JS_PKG_JSON.items()
}

JS_PKG_JSON_LABEXT = {
    k: v
    for k, v in JS_PKG_JSON.items()
    if JS_PKG_DATA[k].get("jupyterlab", {}).get("extension")
}

JS_LABEXT_PY_HOST = {
    k: JS_PKG_DATA[k]["jupyterlab"]["discovery"]["server"]["base"]["name"]
    for k, v in JS_PKG_JSON.items()
    if JS_PKG_DATA[k].get("jupyterlab", {}).get("discovery")
}

JS_PKG_NOT_META = {k: v for k, v in JS_PKG_JSON.items() if k.startswith("_")}

JS_TARBALL = {
    k: JS_PKG_JSON[k].parent
    / f"""{v["name"].replace('@', '').replace("/", "-")}-{v["version"]}.tgz"""
    for k, v in JS_PKG_DATA.items()
    if k not in JS_PKG_NOT_META
}

JS_TSCONFIG = {
    k: v.parent / "tsconfig.json"
    for k, v in JS_PKG_JSON.items()
    if (v.parent / "tsconfig.json").exists()
}

JS_TSSRC = {
    k: sorted(
        [*(v.parent / "src").rglob("*.ts")] + [*(v.parent / "src").rglob("*.tsx")]
    )
    for k, v in JS_TSCONFIG.items()
    if (v.parent / "src").exists()
}

JS_TSBUILDINFO = {k: v.parent / "tsconfig.tsbuildinfo" for k, v in JS_TSCONFIG.items()}

JS_STYLE = {
    k: sorted((v.parent / "style").glob("*.css"))
    for k, v in JS_PKG_JSON.items()
    if (v.parent / "style").exists()
}

JS_PY_SCRIPTS = {
    k: sorted((v.parent / "scripts").glob("*.py"))
    for k, v in JS_PKG_JSON.items()
    if (v.parent / "scripts").exists()
}

# special things for jupyterlab-drawio-webpack
IPDW = JS_PKG_JSON["ipydrawio-webpack"].parent
IPDW_APP = IPDW / "drawio/src/main/webapp/js/app.min.js"
IPDW_PY = (IPDW / "scripts").rglob("*.py")
DRAWIO = IPDW / "drawio"
IPDW_LIB = IPDW / "lib"
IPDW_IGNORE = IPDW / ".npmignore"
ALL_IPDW_JS = IPDW_LIB.glob("*.js")

PY_PACKAGES = ROOT / "py_packages"

PY_SETUP = {p.parent.name: p for p in (ROOT / "py_packages").glob("*/setup.py")}
PY_SRC = {k: sorted((v.parent / "src").rglob("*.py")) for k, v in PY_SETUP.items()}
PY_SETUP_CFG = {k: v.parent / "setup.cfg" for k, v in PY_SETUP.items()}
PY_VERSION = {
    k: re.findall(
        r"""__version__ = "([^"]+)""",
        [vv for vv in v if vv.name == "_version.py"][0].read_text(),
    )[0]
    for k, v in PY_SRC.items()
}

IPD = PY_SETUP["ipydrawio"].parent
IPDE = PY_SETUP["ipydrawio-export"].parent

PY_SDIST = {
    IPDE.name: IPDE / "dist" / f"{IPDE.name}-1.0.0a0.tar.gz",
    IPD.name: IPD / "dist" / f"{IPD.name}-1.0.0a0.tar.gz",
}
PY_WHEEL = {
    IPDE.name: IPDE
    / "dist"
    / f"""{IPDE.name.replace("-", "_")}-1.0.0a0-py3-none-any.whl""",
    IPD.name: IPD
    / "dist"
    / f"""{IPD.name.replace("-", "_")}-1.0.0a0-py3-none-any.whl""",
}
PY_TEST_DEP = {}

SERVER_EXT = {
    k: sorted(v.parent.glob("src/*/serverextension.py"))[0]
    for k, v in PY_SETUP.items()
    if sorted(v.parent.glob("src/*/serverextension.py"))
}


def NOT_LABEXTENSIONS(paths):
    return [p for p in paths if "labextensions" not in str(p)]


ALL_PY = [
    DODO,
    *SCRIPTS.glob("*.py"),
    *sum(JS_PY_SCRIPTS.values(), []),
    *sum(PY_SRC.values(), []),
    *ATEST.rglob("*.py"),
]
ALL_YML = [*ROOT.glob("*.yml"), *CI.rglob("*.yml"), *BINDER.glob("*.yml")]
ALL_JSON = [
    *ROOT.glob("*.json"),
    *PACKAGES.glob("*/*.json"),
    *PACKAGES.glob("*/schema/*.json"),
    *ATEST.glob("fixtures/*.json"),
]
ALL_MD = [
    *ROOT.glob("*.md"),
    *PACKAGES.glob("*/*.md"),
    *NOT_LABEXTENSIONS(PY_PACKAGES.glob("*/*.md")),
]
ALL_TS = sum(JS_TSSRC.values(), [])
ALL_CSS = sum(JS_STYLE.values(), [])
ALL_ROBOT = [*ATEST.rglob("*.robot")]
ALL_PRETTIER = [*ALL_YML, *ALL_JSON, *ALL_MD, *ALL_TS, *ALL_CSS]
ESLINTRC = ROOT / ".eslintrc.js"

RFLINT_OPTS = sum(
    [
        ["--ignore", c]
        for c in [
            "LineTooLong",
            "RequireKeywordDocumentation",
            "TooFewKeywordSteps",
            "RequireKeywordDocumentation",
            "TooFewTestSteps",
        ]
    ],
    [],
)

# package: [dependencies, targets]
JS_PKG_PACK = {k: [[v.parent / "package.json"], [v]] for k, v in JS_TARBALL.items()}
[
    JS_PKG_PACK[k][0].append(v)
    for k, v in JS_TSBUILDINFO.items()
    if not k.startswith("_")
]
JS_PKG_PACK[IPDW.name][0] += [
    IPDW_IGNORE,
    IPDW_APP,
    *ALL_IPDW_JS,
]


# built files
OK_INTEGRITY = BUILD / "integrity.ok"
OK_SUBMODULES = BUILD / "submodules.ok"
OK_BLACK = BUILD / "black.ok"
OK_FLAKE8 = BUILD / "flake8.ok"
OK_ISORT = BUILD / "isort.ok"
OK_LINT = BUILD / "lint.ok"
OK_ROBOTIDY = BUILD / "robot.tidy.ok"
OK_PYFLAKES = BUILD / "pyflakes.ok"
OK_PRETTIER = BUILD / "prettier.ok"
OK_ESLINT = BUILD / "eslint.ok"
OK_JS_BUILD_PRE = BUILD / "js.build.pre.ok"
OK_JS_BUILD = BUILD / "js.build.ok"
OK_PYSETUP = {k: BUILD / f"pysetup.{k}.ok" for k, v in PY_SETUP.items()}
OK_PYTEST = {k: BUILD / f"pytest.{k}.ok" for k, v in PY_SETUP.items()}
OK_SERVEREXT = {k: BUILD / f"serverext.{k}.ok" for k, v in SERVER_EXT.items()}
OK_PROVISION = BUILD / "provision.ok"
OK_ROBOT_DRYRUN = BUILD / "robot.dryrun.ok"
OK_RFLINT = BUILD / "robot.rflint.ok"
OK_ATEST = BUILD / "atest.ok"

OK_EXT_BUILD = {k: BUILD / f"ext.build.{k}.ok" for k in JS_LABEXT_PY_HOST}

PY_TEST_DEP["jupyter-drawio-export"] = [OK_PROVISION]

HASH_DEPS = [*PY_SDIST.values(), *PY_WHEEL.values(), *JS_TARBALL.values()]
SHA256SUMS = DIST / "SHA256SUMS"

# built artifacts
EXAMPLE_HTML = [DIST_NBHTML / p.name.replace(".ipynb", ".html") for p in EXAMPLE_IPYNB]

CMD_LIST_EXTENSIONS = ["jupyter", "labextension", "list"]

CMD_LAB = ["jupyter", "lab", "--no-browser", "--debug"]


def get_atest_stem(attempt=1, extra_args=None, browser=None):
    """get the directory in ATEST_OUT for this platform/apps"""
    browser = browser or "headlessfirefox"
    extra_args = extra_args or []

    stem = f"{PLATFORM}_{PY_MAJOR}_{browser}_{attempt}"

    if "--dryrun" in extra_args:
        stem += "_dry_run"

    return stem
