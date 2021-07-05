*** Settings ***
Documentation     A work-in-progress set of keywords for JupyterLite
Library           OperatingSystem
Library           Process
Library           ../ports.py

*** Variable ***
${NEXT LITE LOG}    ${0}
# TODO: don't hard-code: use unused port, some nasty emoji/space prefixes, etc.
${LITE URL}       http://localhost:8000/lab/index.html

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
    ${p} =    Start JupyterLite Process    serve    ${cwd}    @{args}
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
