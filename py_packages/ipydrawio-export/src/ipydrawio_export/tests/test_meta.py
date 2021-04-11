"""ipydrawio-export metadata tests"""

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

import ipydrawio_export


def test_version():
    assert ipydrawio_export.__version__, "no version"


def test_js():
    assert ipydrawio_export.__js__, "no js metadata"


def test_magic_lab_extensions():
    assert (
        len(ipydrawio_export._jupyter_labextension_paths()) == 1
    ), "too many/few labextensions"


def test_magic_server_extensions():
    assert (
        len(ipydrawio_export._jupyter_server_extension_paths()) == 1
    ), "too many/few serverextensions"
