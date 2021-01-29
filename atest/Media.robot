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
