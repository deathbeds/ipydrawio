""" patch drawio sources for our purposes
"""
from pathlib import Path
import subprocess

HERE = Path(__file__).parent
ROOT = HERE.parent
DRAWIO = ROOT / "drawio"
APP_MIN = DRAWIO / "src/main/webapp/js/app.min.js"
PATCHES = {
    APP_MIN: [
        {
            "name": "global ref",
            "before": "b=null!=e?e():new App(new Editor",
            "after": "\nwindow.JUPYTERLAB_DRAWIO_APP = b=null!=e?e():new App(new Editor"
        }
    ]
}

def patch():
    for path, patches in PATCHES.items():
        print("checkout", path)
        subprocess.check_call(
            ["git", "checkout", str(path.relative_to(DRAWIO))],
            cwd=DRAWIO
        )
        txt = path.read_text()

        for patch in patches:
            print("  ", patch["name"])
            if patch["before"] not in txt:
                print("Couldn't find", patch["before"])
            elif patch["after"] not in txt:
                print("   ...patching")
                txt = txt.replace(patch["before"], patch["after"])
            else:
                print("   ...nothing to do")

        path.write_text(txt)


if __name__ == "__main__":
    patch()
