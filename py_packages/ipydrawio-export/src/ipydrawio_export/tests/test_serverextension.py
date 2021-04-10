import asyncio

import pytest

from .. import load_jupyter_server_extension


@pytest.fixture
def ip_dio_export_app(jp_serverapp):
    load_jupyter_server_extension(jp_serverapp)
    yield jp_serverapp


async def test_serverextension_status(ip_dio_export_app, jp_fetch):
    await jp_fetch("ipydrawio", "status")


async def test_serverextension_provision(ip_dio_export_app, jp_fetch):
    success = False
    retries = 10

    while retries and not success:
        retries -= 1
        try:
            await jp_fetch("ipydrawio", "provision", method="POST", body="")
            success = True
        except Exception as err:  # pragma: no cover
            print(err)
            await asyncio.sleep(5)

    assert success


# async def test_serverextension_export(ip_dio_export_app, jp_fetch):
#     await jp_fetch("ipydrawio", "export", method="POST", body="")
