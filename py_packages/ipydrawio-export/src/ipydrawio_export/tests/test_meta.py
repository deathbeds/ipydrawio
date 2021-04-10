from .. import __version__, _jupyter_labextension_paths, _jupyter_server_extension_paths


def test_version():
    assert __version__


def test_magiclabextensions():
    assert len(_jupyter_labextension_paths()) == 1


def test_magic_serverextensions():
    assert len(_jupyter_server_extension_paths()) == 1
