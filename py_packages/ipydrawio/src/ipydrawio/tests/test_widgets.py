import ipywidgets as W

from ipydrawio import Diagram


def test_widget():
    diagram = Diagram()

    assert isinstance(diagram, W.Box), "it is not a box"
