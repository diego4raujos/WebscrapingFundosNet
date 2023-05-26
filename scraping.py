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

options = Options()
options.add_argument('-headless')

cnpj = '11728688000147'
raw = f'{os.getcwd()}/github_/data/raw/'
os.mkdir(f'{raw}{cnpj}')


def acessa_pagina_web(cnpj):
    navegador = webdriver.Firefox(options=options)
    URL = 'https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM?cnpjFundo='
    navegador.get(''.join([URL, cnpj]))
    time.sleep(2)
    return navegador


def pressiona_botao_exibir_filtros(id):
    exibir_filtros = navegador.find_element(By.ID, id)
    exibir_filtros.click()
    time.sleep(2)


def pressiona_dropdown(id):
    dropdown = navegador.find_element(By.ID, id)
    dropdown.click()
    time.sleep(2)


def informa_valor_campo_texto(id, categoria):
    campo_texto = navegador.find_element(By.ID, id)
    campo_texto.send_keys(categoria, Keys.ENTER)
    time.sleep(2)


def pressiona_botao_filtrar(id):
    filtrar = navegador.find_element(By.ID, id)
    filtrar.click()
    time.sleep(2)


def modifica_numero_registros_visiveis(num, nome):
    mostrar_registros = navegador.find_element(By.NAME, nome)
    registros = Select(mostrar_registros)
    registros.select_by_visible_text(str(num))
    time.sleep(2)


def obtem_links(atributo):
    todos_links = navegador.find_elements(By.TAG_NAME, 'a')
    links = []
    for link in todos_links:
        links.append(link.get_attribute(atributo))
    return links


def remove_tipo_indefinido(lista):
    links_definidos = [link for link in lista if link is not None]
    return links_definidos


def remove_links_invalidos(lista):
    nome_filtro = 'downloadDocumento'
    links = [link for link in lista if nome_filtro in link]
    return links


def download_arquivo(caminho):
    for link in links_validos:
        doc = requests.get(link, allow_redirects=True, verify=True)
        nome = re.findall('filename="(.+)"', doc.headers.get('content-disposition'))[0]
        diretorio = ''.join([caminho, nome])

        with open(diretorio, 'wb') as arquivo:
            arquivo.write(base64.b64decode(doc.content))
        time.sleep(0.5)


navegador = acessa_pagina_web(cnpj)

pressiona_botao_exibir_filtros('showFiltros')

pressiona_dropdown('select2-chosen-2')  # Categoria
informa_valor_campo_texto('s2id_autogen2_search', 'Informes Periódicos')

pressiona_dropdown('select2-chosen-3')  # Tipo
informa_valor_campo_texto('s2id_autogen3_search', 'Informe Mensal Estruturado')

pressiona_dropdown('select2-chosen-5')  # Situação
informa_valor_campo_texto('s2id_autogen5_search', 'Ativo')

pressiona_botao_filtrar('filtrar')
modifica_numero_registros_visiveis(100, 'tblDocumentosEnviados_length')

links = obtem_links('href')

navegador.quit()

links = remove_tipo_indefinido(links)
links_validos = remove_links_invalidos(links)

download_arquivo(f'{raw}{cnpj}/')
print('Download dos arquivos xml concluído')