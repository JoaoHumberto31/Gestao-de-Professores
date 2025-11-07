*** Settings ***
Documentation      Teste para verificar o Login
Library            SeleniumLibrary
Library            OperatingSystem  

*** Variables ***
${URL_BASE}        http://127.0.0.1:5000
${BROWSER}         chrome
${VALID_EMAIL}     pereira@gmail.com
${VALID_PASSWORD}  12345

*** Test Cases ***
Realizar um Login com credenciais válidas
    [Tags]        UI    Login    Sucesso

    # 1 - Abrindo o navegador
    Open Browser     ${URL_BASE}    ${BROWSER}
    Maximize Browser Window
    
    # 2 - Preencher os campos usando os ID do HTML
    Input Text       id=email    ${VALID_EMAIL}
    Input Text       id=senha    ${VALID_PASSWORD}

    Sleep            2s

    # 3 - Clicar no botão de Login
    Click Button     id=btnSubmit

    
    # 4 - Finalizando o teste
    Close Browser