# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#                 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

*** Settings ***
Documentation     Does advanced create work?
Resource          _Keywords.robot
Library           OperatingSystem
Force Tags        component:document    component:advanced-create
Suite Setup       Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}advanced-create

*** Test Cases ***
Defaults
    [Documentation]    Does taking the defaults work?
    Launch Advanced Diagram
    Accept Advanced Options
    Capture Page Screenshot    00-defaults.png
