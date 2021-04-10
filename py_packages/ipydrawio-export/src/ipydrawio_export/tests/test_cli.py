import pytest

from .. import __version__


@pytest.mark.script_launch_mode("subprocess")
def test_cli_version(script_runner):
    ret = script_runner.run("jupyter", "ipydrawio-export", "--version")
    assert ret.success
    assert __version__ in ret.stdout
