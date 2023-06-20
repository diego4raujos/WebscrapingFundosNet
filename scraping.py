# arquivo scraping_oop.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os
import requests
import base64
import re

class WebScraper():

    def __init__(self, cnpj):
        self.cnpj = cnpj
        self.url_base = 'https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM?cnpjFundo='
        self.modo_oculto = Options()
        self.modo_oculto.add_argument('-headless')
        self.navegador = webdriver.Firefox(options=None) # ou self.modo_oculto

    def cria_diretorio(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        else:
            print('Diretório já existente')

    def acessar_pagina_web(self):
        self.navegador.get(f'{self.url_base}{self.cnpj}')
        time.sleep(1)
       
    def pressionar_botao_exibir_filtros(self):
        self.navegador.find_element(By.ID, 'showFiltros').click()
        time.sleep(1)
    
    def pressionar_dropdown(self, id):
        self.navegador.find_element(By.ID, id).click()
        time.sleep(1)

    def informar_valor_campo_texto(self, id, categoria):
        self.navegador.find_element(By.ID, id).send_keys(categoria, Keys.ENTER)
        time.sleep(1)
    
    def pressionar_botao_filtrar(self):
        self.navegador.find_element(By.ID, 'filtrar').click()
        time.sleep(1)
    
    def modificar_numero_registro_pagina(self):
        seletor = Select(self.navegador.find_element(By.NAME, 'tblDocumentosEnviados_length'))
        seletor.select_by_visible_text('100')
        time.sleep(1)
     
    def coletar_links_validos(self):
        seletor = self.navegador.find_elements(By.TAG_NAME, 'a')
        links = [link.get_attribute('href') for link in seletor]
        links_limpos = [link for link in links if link is not None] # remove tipos indefinidos
        return [link for link in links_limpos if 'downloadDocumento' in link] # links de downloads

    def download_arquivo(self, dir, links):
        for link in links:
            doc = requests.get(link, allow_redirects=True, verify=True)
            nome = re.findall('filename="(.+)"', doc.headers.get('content-disposition'))[0]
            path = f'{dir}{nome}'

            with open(path, 'wb') as arquivo:
                arquivo.write(base64.b64decode(doc.content))
            time.sleep(0.5)
            print(nome)

fii = '11728688000147' # cnpj do fundo de investimento imobiliário
caminho = f'{os.getcwd()}/dados/' #'/home/diego/Projetos/WebscrapingFundosNet/dados/'

scraper = WebScraper(fii)
scraper.cria_diretorio(f'{caminho}{fii}')

scraper.acessar_pagina_web()
scraper.pressionar_botao_exibir_filtros()

scraper.pressionar_dropdown('select2-chosen-2') # categoria
scraper.informar_valor_campo_texto('s2id_autogen2_search', 'Informes Periódicos')

scraper.pressionar_dropdown('select2-chosen-3') # tipo
scraper.informar_valor_campo_texto('s2id_autogen3_search', 'Informe Mensal Estruturado')

scraper.pressionar_dropdown('select2-chosen-5') # situação
scraper.informar_valor_campo_texto('s2id_autogen5_search', 'Ativo')

scraper.pressionar_botao_filtrar() # aplica todos os filtros definidos
scraper.modificar_numero_registro_pagina()

links = scraper.coletar_links_validos()
scraper.download_arquivo(f'{caminho}{fii}/', links)