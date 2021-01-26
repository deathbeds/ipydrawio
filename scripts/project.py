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
EXTENSIONS_FILE = BINDER / "labextensions.txt"
OVERRIDES = ROOT / "overrides.json"
EXTENSIONS = sorted(
    [
        line.strip()
        for line in EXTENSIONS_FILE.read_text().strip().splitlines()
        if line and not line.startswith("#")
    ]
)
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
JLPM_INSTALL = [*JLPM, "--ignore-optional", "--prefer-offline"]
LAB_EXT = ["jupyter", "labextension"]
LAB = ["jupyter", "lab"]
PRETTIER = [str(NODE_MODULES / ".bin" / "prettier")]

# lab stuff
LAB_APP_DIR = PREFIX / "share/jupyter/lab"
LAB_STAGING = LAB_APP_DIR / "staging"
LAB_LOCK = LAB_STAGING / "yarn.lock"
LAB_STATIC = LAB_APP_DIR / "static"
LAB_INDEX = LAB_STATIC / "index.html"
LAB_OVERRIDES = LAB_APP_DIR / "settings" / "overrides.json"

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
JDIO = PACKAGES / "jupyterlab-drawio"

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
JDW = JS_PKG_JSON["jupyterlab-drawio-webpack"].parent
JDW_APP = JDW / "drawio/src/main/webapp/js/app.min.js"
JDW_PY = (JDW / "scripts").rglob("*.py")
DRAWIO = JDW / "drawio"
JDW_LIB = JDW / "lib"
JDW_IGNORE = JDW / ".npmignore"
ALL_JDW_JS = JDW_LIB.glob("*.js")

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
JDE = PY_SETUP["jupyter-drawio-export"].parent
PY_SDIST = {JDE.name: JDE / "dist" / f"{JDE.name}-0.8.0a2.tar.gz"}
PY_WHEEL = {
    JDE.name: JDE
    / "dist"
    / f"""{JDE.name.replace("-", "_")}-0.8.0a2-py3-none-any.whl"""
}
PY_TEST_DEP = {}

SERVER_EXT = {
    k: sorted(v.parent.glob("src/*/serverextension.py"))[0]
    for k, v in PY_SETUP.items()
    if sorted(v.parent.glob("src/*/serverextension.py"))
}

# mostly linting
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
    *ATEST.rglob("*.json"),
]
ALL_MD = [*ROOT.glob("*.md"), *PACKAGES.glob("*/*.md"), *PY_PACKAGES.glob("*/*.md")]
ALL_TS = sum(JS_TSSRC.values(), [])
ALL_CSS = sum(JS_STYLE.values(), [])
ALL_ROBOT = [*ATEST.rglob("*.robot")]
ALL_PRETTIER = [*ALL_YML, *ALL_JSON, *ALL_MD, *ALL_TS, *ALL_CSS]

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
JS_PKG_PACK[JDW.name][0] += [
    JDW_IGNORE,
    JDW_APP,
    *ALL_JDW_JS,
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

PY_TEST_DEP["jupyter-drawio-export"] = [OK_PROVISION, LAB_INDEX]

HASH_DEPS = [*PY_WHEEL.values(), *JS_TARBALL.values()]
SHA256SUMS = DIST / "SHA256SUMS"

# built artifacts
EXAMPLE_HTML = [DIST_NBHTML / p.name.replace(".ipynb", ".html") for p in EXAMPLE_IPYNB]

# long lab commands
CMD_LINK_EXTENSIONS = [
    "jupyter",
    "labextension",
    "link",
    "--debug",
    "--no-build",
    *[v.parent for k, v in JS_PKG_JSON_LABEXT.items()],
]

CMD_INSTALL_EXTENSIONS = [
    "jupyter",
    "labextension",
    "install",
    "--debug",
    "--no-build",
    *EXTENSIONS,
]

CMD_INSTALL_ALL_EXTENSIONS = [*CMD_INSTALL_EXTENSIONS, *JS_TARBALL.values()]

CMD_LIST_EXTENSIONS = ["jupyter", "labextension", "list"]

CMD_DISABLE_EXTENSIONS = [
    "jupyter",
    "labextension",
    "disable",
    "@jupyterlab/extension-manager-extension",
]

CMD_BUILD = ["jupyter", "lab", "build", "--debug"]

CMD_LAB = ["jupyter", "lab", "--no-browser", "--debug"]


def _override_lab():
    if LAB_OVERRIDES.exists():
        LAB_OVERRIDES.unlink()

    if not LAB_OVERRIDES.parent.exists():
        LAB_OVERRIDES.parent.mkdir(parents=True)

    shutil.copy2(OVERRIDES, LAB_OVERRIDES)


def get_atest_stem(attempt=1, extra_args=None, browser=None):
    """get the directory in ATEST_OUT for this platform/apps"""
    browser = browser or "headlessfirefox"
    extra_args = extra_args or []

    stem = f"{PLATFORM}_{PY_MAJOR}_{browser}_{attempt}"

    if "--dryrun" in extra_args:
        stem += "_dry_run"

    return stem
