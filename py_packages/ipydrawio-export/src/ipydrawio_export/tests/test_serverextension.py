"""ipydrawio-export serverextension tests"""

# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from urllib.parse import urlencode

import pytest
from tornado.simple_httpclient import HTTPTimeoutError

from .. import load_jupyter_server_extension


@pytest.fixture
def ip_dio_export_app(jp_serverapp):
    load_jupyter_server_extension(jp_serverapp)
    yield jp_serverapp


async def test_serverextension_status(ip_dio_export_app, jp_fetch):
    await jp_fetch("ipydrawio", "status")


async def test_serverextension_export(ip_dio_export_app, jp_fetch, empty_dio):
    success = False
    retries = 10

    while retries and not success:
        retries -= 1
        try:
            await jp_fetch("ipydrawio", "provision", method="POST", body="")
            success = True
        except HTTPTimeoutError as err:  # pragma: no cover
            print(err)
            await asyncio.sleep(5)

    assert success

    success = False
    retries = 10

    while retries and not success:
        retries -= 1
        try:
            await jp_fetch(
                "ipydrawio",
                "export/",
                method="POST",
                body=urlencode(
                    dict(
                        xml=empty_dio.read_text(encoding="utf-8"),
                        format="pdf",
                        base64="1",
                    )
                ),
            )
            success = True
        except HTTPTimeoutError as err:  # pragma: no cover
            print(err)
            await asyncio.sleep(5)

    assert success
