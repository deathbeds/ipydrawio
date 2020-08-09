import re
from pathlib import Path

HERE = Path(__file__).parent

version = re.findall(
    r"""__version__\s*=\s*"([^"]+)""",
    [*HERE.glob("src/*/_version.py")][0].read_text(encoding="utf-8")
)[0]


if __name__ == "__main__":
    import setuptools
    setuptools.setup(version=version)
