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
Documentation     A work-in-progress set of keywords for JupyterLite
Library           OperatingSystem
Library           Process
Library           ../ports.py

*** Variable ***
${NEXT LITE LOG}    ${0}

*** Keywords ***
Start JupyterLite Process
    [Arguments]    ${task}    ${cwd}    @{args}
    [Documentation]    Start a `jupyter lite` process
    ${p} =    Start Process    jupyter    lite    ${task}    @{args}
    ...    cwd=${cwd}    stdout=${OUTPUT DIR}${/}lite-${NEXT LITE LOG}.log    stderr=STDOUT
    Set Global Variable    ${NEXT LITE LOG}    ${NEXT LITE LOG + 1}
    [Return]    ${p}

Start JupyterLite Server
    [Documentation]    Start _the_ `jupyter lite` server
    [Arguments]    ${cwd}    @{args}
    Set Environment Variable    MOZ_HEADLESS    1
    ${prefix} =    Set Variable    /@rf/
    ${port} =    Get Unused Port
    ${url} =    Set Variable    http://localhost:${port}${prefix}lab/index.html
    Set Global Variable    ${LITE URL}    ${url}
    ${p} =    Start JupyterLite Process    serve    ${cwd}
    ...    @{args}    --port    ${port}    --base-url    ${prefix}
    Set Global Variable    ${LITE SERVER}    ${p}
    Close All Browsers
    ${service args} =    Create List    --log    warn
    Create WebDriver    Firefox
    ...    service_log_path=${OUTPUT DIR}${/}geckodriver-lite.log
    ...    service_args=${service args}

Open JupyterLite
    Set Environment Variable    MOZ_HEADLESS    1
    ${service args} =    Create List    --log    warn
    Wait For Splash    ${LITE URL}

Stop JupyterLite Server
    [Documentation]    Stop _the_ `jupyter lite` server
    Close All Browsers
    Terminate Process    ${LITE SERVER}

Start Lite Test
    [Documentation]    Start with a blank browser
    Open JupyterLite

Clean Up Lite Test
    [Documentation]    Clean up
    ...    TODO: how might we clear the application cache?
    Close All Browsers

Start Lite Suite
    [Documentation]    Ensure lite assets are available
    Set Screenshot Directory    ${OUTPUT DIR}${/}lite
    Start JupyterLite Server    ${DEMO}

Clean Up Lite Suite
    [Documentation]    Clean up after lite
    Stop JupyterLite Server
