*** Settings ***
Documentation     Common behaviors for CodeMirror instances

*** Keywords ***
Set CodeMirror Value
    [Arguments]    ${css}    ${code}
    [Documentation]    Set the value in the CodeMirror attached to the element
    ...    that matches a ``css`` selector to be the given ``text``.
    Select All CodeMirror Text    ${css}
    Replace CodeMirror Selection    ${css}    ${code}

Select All CodeMirror Text
    [Arguments]    ${css}
    [Documentation]    Select all of the text in the CodeMirror attached to the element
    ...    matched by a ``css`` selector.
    Execute CodeMirror Command    ${css}    selectAll

Execute CodeMirror Command
    [Arguments]    ${css}    ${cmd}
    [Documentation]    Run a CodeMirror [https://codemirror.net/doc/manual.html#commands:command]
    ...    ``cmd`` for the editor attached to element that matches a ``css`` selector
    Call CodeMirror Method    ${css}    execCommand("${cmd}")

Replace CodeMirror Selection
    [Arguments]    ${css}    ${code}
    [Documentation]    Replace all of the text in the CodeMirror attached to the element
    ...    that matches a ``css`` selector with the given ``text``.
    Call CodeMirror Method    ${css}    replaceSelection(`${code}`)

Call CodeMirror Method
    [Arguments]    ${css}    ${js}
    [Documentation]    Construct and a method call against in the CodeMirror attached to the element
    ...    that matches a ``css`` selector with the given ``js`` code.
    Execute JavaScript    document.querySelector(`${css}`).CodeMirror.${js}
