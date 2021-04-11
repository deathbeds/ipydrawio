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
Documentation     Does the media type (mimerenderer) work?
Resource          _Keywords.robot
Resource          _Notebook.robot
Force Tags        component:media
Library           OperatingSystem

*** Test Cases ***
Drawio XML
    [Documentation]    does native Drawio XML work?
    Validate Media Display    drawio-xml    application/x-drawio    A.dio

*** Keywords ***
Validate Media Display
    [Arguments]    ${label}    ${media type}    ${example}    ${format}=text
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}media${/}${label}
    Set Tags    media:${media type}
    ${path} =    Normalize Path    examples${/}${example}
    Launch Untitled Notebook
    Add and Run JupyterLab Code Cell    from pathlib import Path
    Add and Run JupyterLab Code Cell    from IPython.display import display
    Add and Run JupyterLab Code Cell    data = Path("${path}").read_${format}()
    Add and Run JupyterLab Code Cell    display({"${media type}": data}, {}, raw=True)
    Sleep    5s
    Capture Page Screenshot    99-teardown.png
