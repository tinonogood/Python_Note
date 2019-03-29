*** Settings ***
Library           SeleniumLibrary

*** Test Cases ***
Test1
    Open Browser    http://www.tomato.es/    chrome
    Close Browser
