*** Settings ***
Documentation     Does the media type (mimerenderer) work?
Resource          _Keywords.robot
Force Tags        component:document

*** Test Cases ***
Drawio XML
    [Documentation]    does native Drawio XML work?
    Validate Media Display    drawio-xml    application/x-drawio

*** Keywords ***
Validate Media Display
    [Arguments]    ${label}    ${media type}
    Set Tags    media:${media type}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots${/}media${/}${label}
    Launch Untitled Notebook
    Capture Page Screenshot    99-teardown.png

Launch Untitled Notebook
    Lab Command    New Launcher
    Ensure Sidebar Is Closed
    Click Element    ${XP LAUNCH TAB}
    Wait Until Element is Enabled    ${CSS LAUNCH IPYNB}
    Click Element    ${CSS LAUNCH IPYNB}
