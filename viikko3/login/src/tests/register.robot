*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  matti
    Set Password  matti123
    Set Password Confirmation  matti123
    Click  button >> text=Register
    Welcome Page Should Be Open

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click  button >> text=Register
    Registration Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  kalle
    Set Password  kal
    Set Password Confirmation  kal
    Click  button >> text=Register
    Registration Should Fail With Message  Password must be at least 4 characters long

Register With Password Containing Numbers
    Set Username  matti
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click  button >> text=Register
    Welcome Page Should Be Open

Register With Password Containing Special Characters
    Set Username  pekka
    Set Password  kalle#abc
    Set Password Confirmation  kalle#abc
    Click  button >> text=Register
    Welcome Page Should Be Open

Register With Lowercase Letters Only Password
    Set Username  maija
    Set Password  kallekalle
    Set Password Confirmation  kallekalle
    Click  button >> text=Register
    Registration Should Fail With Message  Password must contain a number or special character

Register With Uppercase Letters Only Password
    Set Username  teemu
    Set Password  KalleKalle
    Set Password Confirmation  KalleKalle
    Click  button >> text=Register
    Registration Should Fail With Message  Password must contain a number or special character

Register With Mismatching Password Confirmation
    Set Username  ville
    Set Password  kalle123
    Set Password Confirmation  kalle456
    Click  button >> text=Register
    Registration Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click  button >> text=Register
    Registration Should Fail With Message  User with username kalle already exists

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Fill Text  id=username  ${username}

Set Password
    [Arguments]  ${password}
    Fill Secret  id=password  $password

Set Password Confirmation
    [Arguments]  ${password}
    Fill Secret  id=password_confirmation  $password

Welcome Page Should Be Open
    Get Title  ==  Welcome to Ohtu Application!

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Get Text  body  *=  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To  ${REGISTER_URL}