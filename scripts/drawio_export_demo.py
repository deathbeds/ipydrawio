import subprocess
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
APP = HERE.parent / "drawio-export"

def main():
    if not (APP / "node_modules").exists():
        subprocess.check_call(["jlpm"], cwd=str(APP))

    proc = subprocess.Popen(["jlpm", "devstart"], cwd=str(APP))
    return proc.wait()

if __name__ == "__main__":
    sys.exit(main())
