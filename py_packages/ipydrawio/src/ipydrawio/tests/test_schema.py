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

import jsonschema
import pytest

from ipydrawio.schema import get_validator


@pytest.fixture
def validator():
    return get_validator()


@pytest.mark.parametrize("example,valid", [[{}, True], [0, False]])
def test_validator(validator, example, valid):
    if valid:
        validator.validate(example)
    else:
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(example)
