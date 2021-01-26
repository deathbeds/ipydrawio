import ipydrawio


def test_version():
    assert ipydrawio.__version__


def test_labextensions():
    assert ipydrawio._jupyter_labextension_paths(), "no labextensions"
