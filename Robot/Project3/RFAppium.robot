*** Settings ***
Library           AppiumLibrary

*** Test Cases ***
OpenAppium
    Open Application    http://localhost:4723/wd/hub    platformName=Android    platformVersion=9    deviceName=test    appPackage=com.android.calculator2    appActivity=.Calculator
    Quit Application
