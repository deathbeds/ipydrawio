""" important project paths

    this should not import anything not in py36+ stdlib, or any local paths
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


import json
import os
import platform
import pprint
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

print_ = pprint.pprint
console = None

try:
    import rich.console
    import rich.markdown

    console = rich.console.Console()
    print_ = console.print

except ImportError:
    pass

LITE_PREFIX = None

try:
    __import__("jupyterlite.manager")
    LITE_PREFIX = "demo_"
except (ImportError, AttributeError) as err:
    print_(err)
    pass


SKIPS = ["checkpoint", "pytest_cache"]


def _clean(*paths_or_globs):
    cleaned = []
    for p_or_g in paths_or_globs:
        paths = [p_or_g] if isinstance(p_or_g, Path) else [*p_or_g]
        for p in paths:
            str_p = str(p)
            skipped = False
            for skip in SKIPS:
                if skip in str_p:
                    skipped = True
            if not skipped:
                cleaned += [p]
    return cleaned


_SESSION = None


# platform
PLATFORM = os.environ.get("FAKE_PLATFORM", platform.system())
WIN = PLATFORM == "Windows"
OSX = PLATFORM == "Darwin"
UNIX = not WIN
PREFIX = Path(sys.prefix)
ENC = dict(encoding="utf-8")

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
PY_MAJOR = "".join(map(str, sys.version_info[:2]))

# demo
BINDER = ROOT / ".binder"
OVERRIDES = BINDER / "overrides.json"
POSTBUILD_PY = BINDER / "postBuild"
ENV_BINDER = BINDER / "environment.yml"

# top-level stuff
NODE_MODULES = ROOT / "node_modules"
PACKAGE = ROOT / "package.json"
PACKAGES = ROOT / "packages"
YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"
YARN_LOCK = ROOT / "yarn.lock"
DODO = ROOT / "dodo.py"
BUILD = ROOT / "build"
DIST = ROOT / "dist"
DOCS = ROOT / "docs"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
SETUP_CFG = ROOT / "setup.cfg"

# external URLs
# archive.org template
CACHE_EPOCH = 0
HTTP_CACHE = BUILD / ".requests-cache"


def A_O(archive_id, url, cache_bust=CACHE_EPOCH):
    return "https://web.archive.org/web/{}/{}#{}".format(archive_id, url, cache_bust)


DIA_FAQ = "https://www.diagrams.net/doc/faq"

FETCHED = BUILD / "fetched"

DIA_URLS = {
    FETCHED
    / "supported-url-parameters.html": (
        A_O(20210425055302, f"{DIA_FAQ}/supported-url-parameters")
    ),
    FETCHED / "embed-mode.html": (A_O(20200924053756, f"{DIA_FAQ}/embed-mode")),
    FETCHED
    / "configure-diagram-editor.html": (
        A_O(20210503071537, f"{DIA_FAQ}/configure-diagram-editor")
    ),
}


# ci
CI = ROOT / ".github"
ENV_CI = CI / "environment.yml"

# tools
PY = ["python"]
PYM = [*PY, "-m"]
PIP = [*PYM, "pip"]
PIP_CHECK_IGNORE = "^(No broken|pylint) "

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
EXAMPLE_IPYNB = _clean(EXAMPLES.rglob("*.ipynb"))

DIST_NBHTML = DIST / "nbsmoke"
ATEST = ROOT / "atest"
ATEST_DIO = _clean(ATEST.rglob("*.dio"), ATEST.rglob("*.dio.svg"))
ATEST_OUT = BUILD / "atest"
ATEST_OUT_XML = "output.xml"

# js packages
JS_NS = "deathbeds"
IPYDIO = PACKAGES / "ipydrawio"
TSCONFIGBASE = PACKAGES / "tsconfigbase.json"
TSCONFIG_TYPEDOC = PACKAGES / "tsconfig.typedoc.json"
TYPEDOC_JSON = PACKAGES / "typedoc.json"
TYPEDOC_CONF = [TSCONFIG_TYPEDOC, TYPEDOC_JSON]
NO_TYPEDOC = ["_meta", "ipydrawio-webpack"]

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


def _norm_js_version(pkg):
    """undo some package weirdness"""
    v = pkg["version"]
    final = ""
    # alphas, beta use dashes
    for dashed in v.split("-"):
        if final:
            final += "-"
        for dotted in dashed.split("."):
            if final:
                final += "."
            if re.findall(r"^\d+$", dotted):
                final += str(int(dotted))
            else:
                final += dotted
    return final


JS_TARBALL = {
    k: JS_PKG_JSON[k].parent
    / f"""{v["name"].replace('@', '').replace("/", "-")}-{_norm_js_version(v)}.tgz"""
    for k, v in JS_PKG_DATA.items()
    if k not in JS_PKG_NOT_META
}

JS_TSCONFIG = {
    k: v.parent / "src/tsconfig.json"
    for k, v in JS_PKG_JSON.items()
    if (v.parent / "src/tsconfig.json").exists()
}

JS_TSSRC = {
    k: sorted(
        [
            *(v.parent).rglob("*.ts"),
            *(v.parent / "src").rglob("*.tsx"),
        ]
    )
    for k, v in JS_TSCONFIG.items()
}

JS_TSBUILDINFO = {
    k: v.parent.parent / ".src.tsbuildinfo" for k, v in JS_TSCONFIG.items()
}

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

JS_SCHEMAS = {
    k: sorted((v.parent / "schema").glob("*.json"))
    for k, v in JS_PKG_JSON.items()
    if (v.parent / "schema").exists()
}

# special things for ipydrawio-webpack
IPDW = JS_PKG_JSON["ipydrawio-webpack"].parent
IPDW_APP = IPDW / "dio/js/app.min.js"
IPDW_PY = (IPDW / "scripts").rglob("*.py")
DRAWIO = IPDW / "drawio"
IPDW_LIB = IPDW / "lib"
IPDW_IGNORE = IPDW / ".npmignore"
ALL_IPDW_JS = IPDW_LIB.glob("*.js")

IPJT = JS_PKG_JSON["ipydrawio-jupyter-templates"].parent
IPJT_TMPL = IPJT / "tmpl"
IPJT_TMPL_DIO = _clean(
    IPJT_TMPL.rglob("*.dio"),
    IPJT_TMPL.rglob("*.dio.svg"),
)

PY_PACKAGES = ROOT / "py_packages"

PY_SETUP = {p.parent.name: p for p in sorted((ROOT / "py_packages").glob("*/setup.py"))}
PY_SRC = {k: sorted((v.parent / "src").rglob("*.py")) for k, v in PY_SETUP.items()}
PY_SETUP_CFG = {k: v.parent / "setup.cfg" for k, v in PY_SETUP.items()}

PY_VERSION = {
    "ipydrawio": JS_PKG_DATA["ipydrawio"]["version"],
    "ipydrawio-export": JS_PKG_DATA["ipydrawio-pdf"]["version"],
}

IPD = PY_SETUP["ipydrawio"].parent
IPDE = PY_SETUP["ipydrawio-export"].parent

IPD_VERSION = PY_VERSION["ipydrawio"]
IPDE_VERSION = PY_VERSION["ipydrawio-export"]

PY_SDIST = {
    IPDE.name: IPDE / "dist" / f"{IPDE.name}-{IPDE_VERSION}.tar.gz",
    IPD.name: IPD / "dist" / f"{IPD.name}-{IPD_VERSION}.tar.gz",
}
PY_WHEEL = {
    IPDE.name: IPDE
    / "dist"
    / f"""{IPDE.name.replace("-", "_")}-{IPDE_VERSION}-py3-none-any.whl""",
    IPD.name: IPD
    / "dist"
    / f"""{IPD.name.replace("-", "_")}-{IPD_VERSION}-py3-none-any.whl""",
}
PY_TEST_DEP = {}

SERVER_EXT = {
    k: sorted(v.parent.glob("src/*/serverextension.py"))[0]
    for k, v in PY_SETUP.items()
    if sorted(v.parent.glob("src/*/serverextension.py"))
}

# demo
DEMO = ROOT / "demo"
DEMO_LITE_JSON = DEMO / "jupyter-lite.json"
DEMO_APPS = ["lab"]
DEMO_BUILD = DEMO / "_output"
DEMO_HASHES = DEMO_BUILD / "SHA256SUMS"
DEMO_ARCHIVE = DEMO_BUILD / "demo-jupyterlite.tgz"

# docs
SPHINX_ARGS = json.loads(os.environ.get("SPHINX_ARGS", "[]"))
DOCS_CONF = DOCS / "conf.py"
ENV_DOCS = DOCS / "environment.yml"
DOCS_BUILD = BUILD / "docs"
DOCS_BUILDINFO = DOCS_BUILD / ".buildinfo"
DOCS_MD = _clean(
    [
        p
        for p in DOCS.rglob("*.md")
        if not (p.parent.name == "ts" or p.parent.parent.name == "ts")
    ]
)
DOCS_DIO = _clean(DOCS.rglob("*.dio"), DOCS.rglob("*.dio.svg"))
DOCS_RST = _clean(DOCS.rglob("*.rst"))
DOCS_IPYNB = _clean(DOCS.rglob("*.ipynb"))
DOCS_SRC = _clean(DOCS_MD, DOCS_RST, DOCS_IPYNB)
DOCS_STATIC = DOCS / "_static"
DOCS_FAVICON_SVG = DOCS_STATIC / "icon.svg"
DOCS_FAVICON_ICO = DOCS_STATIC / "favicon.ico"
DOCS_TS = DOCS / "api/ts"
DOCS_TS_MYST_INDEX = DOCS_TS / "index.md"
DOCS_TS_MODULES = [
    ROOT / "docs/api/ts" / f"{p.parent.name}.md"
    for p in JS_PKG_JSON.values()
    if p.parent.name not in NO_TYPEDOC
]

DOCS_RAW_TYPEDOC = BUILD / "typedoc"
DOCS_RAW_TYPEDOC_README = DOCS_RAW_TYPEDOC / "README.md"
MD_FOOTER = """
```
Copyright 2021 ipydrawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
"""

# collections, mostly for linting
ALL_PY = [
    *ATEST.rglob("*.py"),
    *BINDER.glob("*.py"),
    *IPDW_PY,
    *PY_SETUP.values(),
    *SCRIPTS.glob("*.py"),
    *sum(JS_PY_SCRIPTS.values(), []),
    *sum(PY_SRC.values(), []),
    DODO,
    POSTBUILD_PY,
    DOCS_CONF,
]
ALL_YML = [
    *ROOT.glob("*.yml"),
    *CI.rglob("*.yml"),
    *BINDER.glob("*.yml"),
    *DOCS.rglob("*.yml"),
]
ALL_JSON = [
    *ROOT.glob("*.json"),
    *PACKAGES.glob("*/*.json"),
    *PACKAGES.glob("*/schema/*.json"),
    *ATEST.glob("fixtures/*.json"),
    *BINDER.glob("*.json"),
    *[p for p in DEMO.rglob("*.json") if "/_output/" not in str(p)],
]
ALL_DIO = [*DOCS_DIO, *IPJT_TMPL_DIO, *ATEST_DIO]
ALL_MD = [*ROOT.glob("*.md"), *PACKAGES.glob("*/*.md"), *DOCS_MD]
ALL_SETUP_CFG = [SETUP_CFG, *PY_SETUP_CFG.values()]
ALL_JS = [PACKAGES / ".eslintrc.js"]
ALL_TS = sum(JS_TSSRC.values(), [])
ALL_CSS = [*sum(JS_STYLE.values(), []), *DOCS.rglob("*.css")]
ALL_ROBOT = [*ATEST.rglob("*.robot")]
ALL_PRETTIER = [*ALL_YML, *ALL_JSON, *ALL_MD, *ALL_TS, *ALL_CSS, *ALL_JS]
ALL_HEADERS = _clean(
    ALL_SETUP_CFG,
    ALL_PY,
    ALL_TS,
    ALL_CSS,
    ALL_JS,
    ALL_MD,
    ALL_YML,
    ALL_ROBOT,
)
ESLINTRC = PACKAGES / ".eslintrc.js"

RFLINT_OPTS = sum(
    [
        ["--ignore", c]
        for c in [
            "FileTooLong",
            "LineTooLong",
            "RequireKeywordDocumentation",
            "RequireKeywordDocumentation",
            "TooFewKeywordSteps",
            "TooFewTestSteps",
            "TooManyTestSteps",
        ]
    ],
    [],
)

# package: [dependencies, targets]
JS_PKG_PACK = {
    k: [[v.parent / "package.json", *v.parent.glob("schema/*.json")], [v]]
    for k, v in JS_TARBALL.items()
}
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

# provisioning stuff
IPYDRAWIO_DATA_DIR = Path(sys.prefix) / "share/jupyter/ipydrawio_export"

# built files
OK_PIP_CHECK = BUILD / "pip.check.ok"
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
OK_DIOLINT = BUILD / "dio.lint.ok"
OK_ATEST = BUILD / "atest.ok"
OK_CONDA_TEST = BUILD / "conda-build.test.ok"
OK_LINK_CHECK = BUILD / "pytest-check-links.ok"

OK_EXT_BUILD = {k: BUILD / f"ext.build.{k}.ok" for k in JS_LABEXT_PY_HOST}

PY_TEST_DEP.setdefault("ipydrawio-export", []).append(OK_PROVISION)

HASH_DEPS = [*PY_SDIST.values(), *PY_WHEEL.values(), *JS_TARBALL.values()]
SHA256SUMS = DIST / "SHA256SUMS"

# built artifacts
EXAMPLE_HTML = [DIST_NBHTML / p.name.replace(".ipynb", ".html") for p in EXAMPLE_IPYNB]

CMD_LIST_EXTENSIONS = ["jupyter", "labextension", "list"]

CMD_LAB = ["jupyter", "lab", "--no-browser", "--debug"]

# conda building
RECIPE = ROOT / "conda.recipe/meta.yaml"
CONDA_BLD = BUILD / "conda-bld"
CONDARC = CI / ".condarc"
# could be mambabuild
CONDA_BUILDERER = os.environ.get("CONDA_BUILDERER", "build")
CONDA_BUILD_ARGS = [
    "conda",
    CONDA_BUILDERER,
    "--override-channels",
    "-c",
    "conda-forge",
]
CONDA_PKGS = {
    pkg: CONDA_BLD / f"noarch/{pkg}-{ver}-py_0.tar.bz2"
    for pkg, ver in PY_VERSION.items()
}

# env inheritance
ENV_INHERITS = {ENV_BINDER: [ENV_CI, ENV_DOCS], ENV_DOCS: [ENV_CI]}


def get_atest_stem(attempt=1, extra_args=None, browser=None):
    """get the directory in ATEST_OUT for this platform/apps"""
    browser = browser or "headlessfirefox"
    extra_args = extra_args or []

    stem = f"{PLATFORM}_{PY_MAJOR}_{browser}_{attempt}"

    if "--dryrun" in extra_args:
        stem += "_dry_run"

    return stem


def ensure_session():
    global _SESSION

    if _SESSION is None:
        try:
            import requests_cache

            _SESSION = requests_cache.CachedSession(cache_name=str(HTTP_CACHE))
        except ImportError:
            import requests

            _SESSION = requests.Session()


def fetch_one(url, path):
    import doit

    yield dict(
        uptodate=[doit.tools.config_changed({"url": url})],
        name=path.name,
        actions=[
            (doit.tools.create_folder, [HTTP_CACHE]),
            (doit.tools.create_folder, [path.parent]),
            (ensure_session, []),
            lambda: [path.write_bytes(_SESSION.get(url).content), None][-1],
        ],
        targets=[path],
    )


def patch_one_env(source, target):
    print("env", source)
    print("-->", target)
    source_text = source.read_text(encoding="utf-8")
    name = re.findall(r"name: (.*)", source_text)[0]

    comment = f"  ### {name}-deps ###"
    old_target = target.read_text(encoding="utf-8").split(comment)
    new_source = source_text.split(comment)
    target.write_text(
        "\n".join(
            [
                old_target[0].strip(),
                comment,
                new_source[1],
                comment.rstrip(),
                old_target[2],
            ]
        )
    )


def typedoc_conf():
    typedoc = json.loads(TYPEDOC_JSON.read_text(**ENC))
    original_entry_points = sorted(typedoc["entryPoints"])
    new_entry_points = sorted(
        [
            str(
                (
                    p.parent / "src/index.ts"
                    if (p.parent / "src/index.ts").exists()
                    else p.parent / "lib/index.d.ts"
                )
                .relative_to(ROOT)
                .as_posix()
            )
            for p in JS_PKG_JSON.values()
            if p.parent.name not in NO_TYPEDOC
        ]
    )

    if json.dumps(original_entry_points) != json.dumps(new_entry_points):
        typedoc["entryPoints"] = new_entry_points
        TYPEDOC_JSON.write_text(json.dumps(typedoc, indent=2, sort_keys=True), **ENC)

    tsconfig = json.loads(TSCONFIG_TYPEDOC.read_text(**ENC))
    original_references = tsconfig["references"]
    new_references = sum(
        [
            [
                {"path": f"./{p.parent.name}/src"},
                {"path": f"./{p.parent.name}"},
            ]
            for p in JS_PKG_JSON.values()
            if p.parent.name not in NO_TYPEDOC
        ],
        [],
    )

    if json.dumps(original_references) != json.dumps(new_references):
        tsconfig["references"] = new_references
        TSCONFIG_TYPEDOC.write_text(
            json.dumps(tsconfig, indent=2, sort_keys=True), **ENC
        )


def mystify():
    """unwrap monorepo docs into per-module docs"""
    mods = defaultdict(lambda: defaultdict(list))
    if DOCS_TS.exists():
        shutil.rmtree(DOCS_TS)

    def mod_md_name(mod):
        return mod.replace("@jupyterlite/", "") + ".md"

    for doc in sorted(DOCS_RAW_TYPEDOC.rglob("*.md")):
        if doc.parent == DOCS_RAW_TYPEDOC:
            continue
        if doc.name == "README.md":
            continue
        doc_text = doc.read_text(**ENC)
        doc_lines = doc_text.splitlines()
        mod_chunks = doc_lines[0].split(" / ")
        src = mod_chunks[1]
        if src.startswith("["):
            src = re.findall(r"\[(.*)/src\]", src)[0]
        else:
            src = src.replace("/src", "")
        pkg = f"""@jupyterlite/{src.replace("/src", "")}"""
        mods[pkg][doc.parent.name] += [
            str(doc.relative_to(DOCS_RAW_TYPEDOC).as_posix())[:-3]
        ]

        # rewrite doc and write back out
        out_doc = DOCS_TS / doc.relative_to(DOCS_RAW_TYPEDOC)
        if not out_doc.parent.exists():
            out_doc.parent.mkdir(parents=True)

        out_text = "\n".join([*doc_lines[1:], ""]).replace("README.md", "index.md")
        out_text = re.sub(
            r"## Table of contents(.*?)\n## ",
            "\n## ",
            out_text,
            flags=re.M | re.S,
        )
        out_text = out_text.replace("/src]", "]")
        out_text = re.sub("/src$", "", out_text, flags=re.M)
        out_text = re.sub(
            r"^((Implementation of|Overrides|Inherited from):)",
            "_\\1_",
            out_text,
            flags=re.M | re.S,
        )
        out_text = re.sub(
            r"^Defined in: ([^\n]+)$",
            "_Defined in:_ `\\1`",
            out_text,
            flags=re.M | re.S,
        )

        out_text += MD_FOOTER

        out_doc.write_text(out_text, **ENC)

    for mod, sections in mods.items():
        out_doc = DOCS_TS / mod_md_name(mod)
        mod_lines = [f"""# `{mod.replace("@jupyterlite/", "")}`\n"""]
        for label, contents in sections.items():
            mod_lines += [
                f"## {label.title()}\n",
                "```{toctree}",
                ":maxdepth: 1",
                *contents,
                "```\n",
                MD_FOOTER,
            ]
        out_doc.write_text("\n".join(mod_lines))

    DOCS_TS_MYST_INDEX.write_text(
        "\n".join(
            [
                "# `@deathbeds/ipydrawio`\n",
                "```{toctree}",
                ":maxdepth: 1",
                *[mod_md_name(mod) for mod in sorted(mods)],
                "```",
                MD_FOOTER,
            ]
        ),
        **ENC,
    )


def pip_check():
    proc = subprocess.Popen([*PIP, "check"], stdout=subprocess.PIPE)
    proc.wait()
    out = proc.stdout.read().decode("utf-8")
    print(out)
    lines = [
        line
        for line in out.splitlines()
        if line.strip() and not re.findall(PIP_CHECK_IGNORE, line)
    ]
    return not len(lines)


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
    import rich.markdown

    for arg in args:
        print_(arg()) if callable(arg) else print_(arg)
    for kw, kwarg in kwargs.items():
        print_(rich.markdown.Markdown(f"# {kw}") if console else kw)
        print_(kwarg()) if callable(kwarg) else print_(kwarg)


def _copy_one(src, dest):
    if not src.exists():
        return False
    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def _build_lite():
    lite = ["jupyter", "lite"]
    args = ["--debug", "--apps", "lab", "--files", "."]
    for act in ["build", "check", "archive"]:
        act_args = list(map(str, [*lite, act, *args]))
        if subprocess.call(act_args, cwd=DEMO) != 0:
            return False


# Late environment hacks
os.environ.update(
    CONDARC=str(CONDARC),
    IPYDRAWIO_DATA_DIR=str(IPYDRAWIO_DATA_DIR),
    PIP_DISABLE_PIP_VERSION_CHECK="1",
)
