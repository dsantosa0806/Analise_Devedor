from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd

from Navegador.selenium_execution import acessa_sior, login, acessa_tela_incial_analise_devedor, analisa


def option_navegador():

    options = webdriver.ChromeOptions()
    options.add_argument("enable-automation")
    ## Provoca um BUG Maluco
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    ## options.page_load_strategy = "none"
    download_path = r'C:\Robot autos'
    options.add_experimental_option('prefs', {
        "download.default_directory": download_path,  # change default directory for downloads
        "download.prompt_for_download": False,  # to auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # it will not show PDF directly in chrome
    })
    return options


def service_navegador():
    serv = Service(ChromeDriverManager().install())
    return serv


navegador = webdriver.Chrome(options=option_navegador(),service=service_navegador())

acessa_sior(navegador)
login(navegador,'','')
acessa_tela_incial_analise_devedor(navegador)

table = pd.read_excel('tables/devedor.xlsx')

# Atribuindo dados para variáveis
for i, devedor in enumerate(table['Devedor']):
    qtde_aits_prevista = int(table.loc[i,'Qtde'])

    if analisa(navegador,devedor,qtde_aits_prevista) == 1:
        acessa_tela_incial_analise_devedor(navegador)
        continue

    # Finaliza o Loop
    acessa_tela_incial_analise_devedor(navegador)

