import pytest

from ..app import ProvisionApp


@pytest.fixture
def provision_app(tmp_path):
    app = ProvisionApp()
    app.drawio_manager.drawio_export_workdir = str(tmp_path)
    yield app
    app.drawio_manager.stop_server()


def test_provision(provision_app, tmp_path):
    provision_app.start()
    assert [*tmp_path.glob("*")]
