import pytest

from .. import load_jupyter_server_extension


@pytest.fixture
def ip_dio_export_app(jp_serverapp):
    load_jupyter_server_extension(jp_serverapp)
    return jp_serverapp


async def test_serverextension_init(ip_dio_export_app, jp_fetch):
    await jp_fetch("ipydrawio", "status")


async def test_serverextension_provision(ip_dio_export_app, jp_fetch):
    await jp_fetch("ipydrawio", "provision", method="POST", body="")


# async def test_serverextension_export(ip_dio_export_app, jp_fetch):
#     await jp_fetch("ipydrawio", "export", method="POST", body="")
