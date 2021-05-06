"""minimal tests of schema"""

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

import pytest

from ipydrawio.schema import get_validator

validator = get_validator()


@pytest.mark.parametrize(
    "example,expected_errors",
    [
        [{}, 0],
        [0, 1],
        *[
            [{p: v["default"]}, 0]
            for p, v in validator.schema["properties"].items()
            if "default" in v
        ],
    ],
)
def test_validator(example, expected_errors):
    errors = [*validator.iter_errors(example)]
    if errors and not expected_errors:
        [print(e.__dict__) for e in errors]
    assert len(errors) == expected_errors
