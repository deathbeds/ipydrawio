""" important project paths

    this should not import anything not in py36+ stdlib, or any local paths
"""
import os
import platform
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

# top-level stuff
NODE_MODULES = ROOT / "node_modules"
PACKAGE = ROOT / "package.json"
YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"
YARN_LOCK = ROOT / "yarn.lock"
EXTENSIONS = BINDER / "labextensions.txt"
CI = ROOT / ".github"
DODO = ROOT / "dodo.py"
BUILD = ROOT / "build"
DIST = ROOT / "dist"

# tools
PY = ["python"]
PYM = [*PY, "-m"]
PIP = [*PYM, "pip"]

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

# tests
EXAMPLES = ROOT / "notebooks"
EXAMPLE_IPYNB = [
    p for p in EXAMPLES.rglob("*.ipynb") if ".ipynb_checkpoints" not in str(p)
]
DIST_NBHTML = DIST / "nbsmoke"

# mostly linting
ALL_PY = [DODO, *SCRIPTS.glob("*.py")]
ALL_YML = [*ROOT.glob("*.yml"), *CI.rglob("*.yml")]
ALL_JSON = [*ROOT.glob("*.json")]
ALL_MD = [*ROOT.glob("*.md")]
ALL_PRETTIER = [*ALL_YML, *ALL_JSON, *ALL_MD]


# built files
OK_BLACK = BUILD / "black.ok"
OK_FLAKE8 = BUILD / "flake8.ok"
OK_ISORT = BUILD / "isort.ok"
OK_LINT = BUILD / "lint.ok"
OK_PYFLAKES = BUILD / "pyflakes.ok"
OK_PRETTIER = BUILD / "prettier.ok"
OK_ESLINT = BUILD / "eslint.ok"

# built artifacts
EXAMPLE_HTML = [DIST_NBHTML / p.name.replace(".ipynb", ".html") for p in EXAMPLE_IPYNB]
