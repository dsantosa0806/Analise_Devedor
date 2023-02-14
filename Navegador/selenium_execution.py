import sys
import time
from datetime import datetime, date
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

## Oh Lord, forgive me for what i'm about to Code !


def acessa_sior(navegador):
    try:
        #Acesso a tela de login
        url_login = 'http://servicos.dnit.gov.br/sior/Account/Login/?ReturnUrl=%2Fsior%2F'
        navegador.get(url_login)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_sior ')
        sys.exit()


def login(navegador,usuario,senha):
    username = usuario
    userpass = senha
    cpfpath = '// *[ @ id = "UserName"]'
    senhapath = '//*[@id="Password"]'
    clickpath = '//*[@id="FormLogin"]/div[4]/div[2]/button'
    err = True
    while err:
        try:
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, cpfpath))).send_keys(username)
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, senhapath))).send_keys(userpass)
            WebDriverWait(navegador, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, clickpath))).click()

            time.sleep(2)

            err = False

        except TimeoutException:
            print('Erro', 'O SIOR apresentou instabilidade, '
                          'por favor reinicie a aplicação e tente novamente T:Login')
            sys.exit()


def validate_login_error(navegador):
    cpfpath = '// *[ @ id = "UserName"]'
    senhapath = '//*[@id="Password"]'
    login_error = '//*[@id="placeholder"]/div[3]/div/div/div/div'
    try:
        navegador.find_element(By.XPATH,login_error).is_displayed()
        navegador.find_element(By.XPATH,cpfpath).clear()
        navegador.find_element(By.XPATH,senhapath).clear()
        return True
    except NoSuchElementException:
        return False


def validate_logado(navegador):
    logado = '//*[@id="center-pane"]/div/div/div[1]/div[2]'
    try:
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, logado))).is_displayed()
        valor = navegador.find_element(By.XPATH, logado).text
        print('Sucesso !', f'Bem-vindo(a)\n'
                           '\n'
                           f' {valor}')
        return True

    except TimeoutException:
        print('Opss', 'O SIOR apresentou instabilidade, a aplicação será encerrada.'
                      ' Por favor reinicie a aplicação e tente novamente T:validate_logado')
        return 0


def acessa_tela_incial_auto(navegador):
    # Acessa a tela da notificação da autuação
    url_base = 'https://servicos.dnit.gov.br/sior/Infracao/ConsultaAutoInfracao/?SituacoesInfracaoSelecionadas=1'
    try:
        navegador.get(url_base)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_tela_incial_auto')
        sys.exit()


def acessa_tela_incial_analise_devedor(navegador):
    # Acessa a tela da notificação da autuação
    url_base = 'https://servicos.dnit.gov.br/sior/Cobranca/AnaliseCondicaoDevedor/?Bind=true'
    try:
        navegador.get(url_base)
    except ValueError:
        print('Erro', 'O SIOR apresentou instabilidade, '
                      'por favor reinicie a aplicação e tente novamente T:acessa_tela_incial_auto')
        sys.exit()


def analisa(navegador, devedor, quantidade):
    input_devedor = '//*[@id="Devedor"]'
    btn_consultar = '//*[@id="placeholder"]/div[1]/div/div[1]/button'
    quant_autos = '//*[@id="gridAnaliseCondicaoDevedor"]/table/tbody/tr/td[4]'
    valor_total = '//*[@id="gridAnaliseCondicaoDevedor"]/table/tbody/tr/td[5]'
    btn_analisar = '//*[@id="gridAnaliseCondicaoDevedor"]/table/tbody/tr/td[6]/button'
    btn_pesquisa_devedor = '//*[@id="btnConsultaCPFDevedorCobranca"]'
    txt_situacao_cad_devedor = '//*[@id="devedorCobrancaSituacaoView"]'
    txt_data_nasc_devedor = '//*[@id="devedorCobrancaDataNascimentoView"]'
    radio_apto = '//*[@id="Resultado_2"]'
    radio_inapto = '//*[@id="Resultado_3"]'
    btn_cancelar_analise = '/html/body/div[8]/div[2]/div[1]/div/div/button[2]'
    btn_confirmar_analise = '/html/body/div[8]/div[2]/div[1]/div/div/button[1]'
    txt_devedor = '//*[@id="gridAnaliseCondicaoDevedor"]/table/tbody/tr/td[3]'
    txt_final_loop = '//*[@id="gridAnaliseCondicaoDevedor"]/div[1]'

    # Input devedor
    try:
        WebDriverWait(navegador, 50).until(
            EC.element_to_be_clickable((By.XPATH, input_devedor))).send_keys(devedor)
    except TimeoutException:
        print(f'Erro {devedor}', 'Input devedor')
        return 1

    # Clique BTN Consultar
    try:
        WebDriverWait(navegador, 40).until(
            EC.element_to_be_clickable((By.XPATH, btn_consultar))).click()

        err = True
        while err:
            time.sleep(1)
            text = WebDriverWait(navegador, 40).until(
                EC.presence_of_element_located((By.XPATH, txt_devedor))).text
            if devedor in text:
                err = False
            else:
                err = True

    except TimeoutException:
        print(f'Erro {devedor}', 'Btn Consultar')
        return 1

    # Aqui deve-se analisar a Quantidade e o Piso
    try:
        qtde = WebDriverWait(navegador, 40).until(
            EC.presence_of_element_located((By.XPATH, quant_autos))).text
        valor = WebDriverWait(navegador, 40).until(
            EC.presence_of_element_located((By.XPATH, valor_total))).text

        if int(qtde) != quantidade:
            print(f'Erro {devedor}', 'A quantidade do SIOR é diferente da quantidade liberada')
            return 1
        elif float(valor.replace('.','').replace(',','.')) < 800.0:
            print(f'Erro {devedor}', 'Valor total abaixo do piso')
            return 1

    except TimeoutException:
        print(f'Erro {devedor}', 'Btn Consultar')
        return 1

    # Clique BTN Analisar
    try:
        WebDriverWait(navegador, 40).until(
            EC.element_to_be_clickable((By.XPATH, btn_analisar))).click()
    except TimeoutException:
        print(f'Erro {devedor}', 'Btn Analisar')
        return 1

    # Clique BTN Consulta API
    try:
        WebDriverWait(navegador, 40).until(
            EC.element_to_be_clickable((By.XPATH, btn_pesquisa_devedor))).click()
    except TimeoutException:
        print(f'Erro {devedor}', 'Btn Consulta API')
        return 1

    #  Situacao Devedor
    try:

        err = True
        while err:
            time.sleep(1)
            nao_informado = WebDriverWait(navegador, 25).until(
                EC.presence_of_element_located((By.XPATH, txt_situacao_cad_devedor))).text

            if nao_informado == 'Não informado':
                err = True
            else:
                err = False

        situacao_devedor = WebDriverWait(navegador, 40).until(
            EC.presence_of_element_located((By.XPATH, txt_situacao_cad_devedor))).text

        data_nasc = WebDriverWait(navegador, 40).until(
            EC.presence_of_element_located((By.XPATH, txt_data_nasc_devedor))).text

        data_nascf = datetime.strptime(data_nasc, '%d/%m/%Y').date()
        ano = int(data_nascf.strftime("%Y"))
        ano_atual = int(date.today().strftime("%Y"))
        idade_devedor = ano_atual - ano

        if situacao_devedor != 'Regular (0)':
            print(f'Erro {devedor}', 'Situação devedor não é regular')
            return 1

        elif idade_devedor >= 80:
            print(f'Erro {devedor}', 'Maior de 80 anos')
            return 1

        # Clique BTN apto
        try:
            WebDriverWait(navegador, 40).until(
                EC.element_to_be_clickable((By.XPATH, radio_apto))).click()
        except TimeoutException:
            print(f'Erro {devedor}', 'Btn Consulta API')
            return 1

        # Clique BTN Confirmar
        try:
            WebDriverWait(navegador, 40).until(
                EC.element_to_be_clickable((By.XPATH, btn_confirmar_analise))).click()
        except TimeoutException:
            print(f'Erro {devedor}', 'Btn Consulta API')
            return 1

        print(f'{devedor} ({situacao_devedor}): {quantidade}/{qtde} R$ {valor} - Idade {idade_devedor}')

        # Clique Busca texto não encontrado
        try:
            err = True
            while err:
                time.sleep(1)
                nao_encontrado = WebDriverWait(navegador, 120).until(
                    EC.presence_of_element_located((By.XPATH, txt_final_loop))).text

                if nao_encontrado == 'Nenhum registro encontrado!':
                    err = False
                    time.sleep(1)
                else:
                    err = True
                    time.sleep(1)
        except TimeoutException:
            print(f'Erro {devedor}', 'Buscando Nenhum Registro encontrado')
            return 1
    except TimeoutException:
        print(f'Erro {devedor}', 'Erro Geral Situação devedor')
        return 1


