from pathlib import Path

from ._version import __version__


def _jupyter_labextension_paths():
    here = Path(__file__).parent

    return [
        dict(
            src=f"{pkg.parent.relative_to(here).as_posix()}",
            dest=pkg.parent.parent.name / pkg.parent.name,
        )
        for pkg in (here / "labextensions").glob("*/*/package.json")
    ]


__all__ = ["__version__"]
