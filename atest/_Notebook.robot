*** Settings ***
Resource          ./_Variables.robot
Resource          ./_CodeMirror.robot

*** Keywords ***
Add and Run JupyterLab Code Cell
    [Arguments]    ${code}=print("hello world")
    [Documentation]    Add a ``code`` cell to the currently active notebook and run it.
    Click Element    css:${JLAB CSS NB TOOLBAR} ${JLAB CSS ICON ADD}
    Sleep    0.1s
    ${cell} =    Get WebElement    css:${JLAB CSS ACTIVE INPUT}
    Click Element    ${cell}
    Set CodeMirror Value    ${JLAB CSS ACTIVE INPUT}    ${code}
    Run Current JupyterLab Code Cell
    Click Element    ${cell}

Wait Until JupyterLab Kernel Is Idle
    [Documentation]    Wait for a kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${JLAB CSS BUSY KERNEL}
    Wait Until Page Does Not Contain    ${JLAB TEXT BUSY PROMPT}

Save JupyterLab Notebook
    Lab Command    Save Notebook

Run Current JupyterLab Code Cell
    Click Element    css:${JLAB CSS ICON RUN}
    Sleep    0.5s
