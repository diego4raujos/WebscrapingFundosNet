from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import re
import requests
import base64
import os

cnpj = '26502794000185'
os.mkdir(f'{os.getcwd()}/dados/{cnpj}') # '../WebScrapingFundosNet/dados/...'

opcao = Options()
opcao.add_argument('-headless') # browser oculto

def inicializar_pagina_web(cnpj):
    navegador = webdriver.Firefox(options=None) # ou opcao
    URL = 'https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM?cnpjFundo='
    navegador.get(f'{URL}{cnpj}')
    time.sleep(2)
    return navegador

def pressionar_botao_exibir_filtros():
    navegador.find_element(By.ID, 'showFiltros').click()
    time.sleep(2)

def pressionar_dropdown(id):
    navegador.find_element(By.ID, id).click()
    time.sleep(2)

def preencher_campo_texto(id, filtro):
    navegador.find_element(By.ID, id).send_keys(filtro, Keys.ENTER)
    time.sleep(2)

def pressionar_botao_filtrar():
    navegador.find_element(By.ID, 'filtrar').click()
    time.sleep(2)

def modificar_numero_registros():
    num_registros = navegador.find_element(By.NAME, 'tblDocumentosEnviados_length')
    registros = Select(num_registros)
    registros.select_by_visible_text(str(100))
    time.sleep(2)

def coletar_links():
    seletor = navegador.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in seletor]
    links_limpos = [link for link in links if link is not None]
    return [link for link in links_limpos if 'downloadDocumento' in link]

def download_arquivo(path, links):
    for link in links:
        doc = requests.get(url=link, allow_redirects=True, verify=True)
        nome = re.findall('filename="(.+)"', doc.headers.get('content-disposition'))[0]
        with open(f'{path}{nome}', 'wb') as arquivo:
            arquivo.write(base64.b64decode(doc.content))
        time.sleep(0.5)

navegador = inicializar_pagina_web(cnpj)

pressionar_botao_exibir_filtros()
pressionar_dropdown('select2-chosen-2')  # Categoria
preencher_campo_texto('s2id_autogen2_search', 'Informes Periódicos')
pressionar_dropdown('select2-chosen-3')  # Tipo
preencher_campo_texto('s2id_autogen3_search', 'Informe Mensal Estruturado')
pressionar_dropdown('select2-chosen-5')  # Situação
preencher_campo_texto('s2id_autogen5_search', 'Ativo')
pressionar_botao_filtrar()
modificar_numero_registros()
download_arquivo(f'{os.getcwd()}/dados/{cnpj}/', coletar_links())