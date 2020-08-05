from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.resolve()
DRAWIO = ROOT / "drawio"
IGNORE = ROOT / ".npmignore"
IGNORED = [
    glob.strip().split("*")[0] if "*" in glob else glob.strip()
    for glob in IGNORE.read_text().strip().splitlines()
    if glob.startswith("drawio/src")
]
STATIC = ROOT / "lib" / "_static.js"
HEADER = """
/**
    All files that should be copied to the jupyterlab static folder, available as:

    {:base_url}static/lab/node_modules/@deathbeds/jupyterlab-drawio-webpack/src/{:path}

    This file generated from https://github.com/jgraph/drawio
*/
"""
TMPL = """
import '!!file-loader?name=[path][name].[ext]&context=.!../drawio{}';
"""

print(IGNORED)

def is_ignored(path):
    for ignore in IGNORED:
        if ignore in str(path):
            return True
    return False

def update_static():
    lines = []

    for path in sorted(DRAWIO.rglob("*")):
        if path.is_dir():
            continue
        if is_ignored(path):
            continue
        lines += [TMPL.format(str(path).replace(str(DRAWIO), "")).strip()]

    STATIC.write_text("\n".join([HEADER, *lines]))
    print(f"wrote {len(lines)} lines")

if __name__ == "__main__":
    update_static()
