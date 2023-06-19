# Automação de Downloads de Informes Mensais do sistema Fundos.NET

## Descrição
Este repositório contém um projeto que usa Python para automatizar o processo de download de informes mensais estruturados de Fundos de Investimento Imobiliário (Fii's) do sistema FundosNet. Fez-se o uso das bibliotecas Requests e Selenium. O projeto possui apenas fins educacionais e informativo.


## Características
1. **Web Scraping**: são utilizadas técnicas de web scraping para navegar entre os elementos HTML que compõem a estrutura da página web e extrair os links necessários para o processo de download dos informes mensais.
2. **Automação Web**: são utilizados recursos da biblioteca Selenium para controlar, de maneira automática, o funcionamento/interação da página web no navegador como cliques em botões e dropdown, preenchimento de campo de texto e downlods de arquivos para a máquina local.

## Requisitos
Python 3.10.6 instalado no seu sistema.
Biblioteca Python: Requests e Selenium.
Navegador Mozilla Firefox instalado na sua máquina.

## Como utilizá-lo
1. Clone o repositório.
```
git clone https://github.com/diego4raujos/WebscrapingFundosNet.git
```
2. Instale as bibliotecas/dependências Python necessárias.
```
pip install -r requirements.txt
```
3. Execute o script "scraping.py" para iniciar a extração dos dados e automação dos downloads.
```
python3 scraping.py
```
4. Abra o arquivo "scraping.ipynb" para verificar, de maneira detalhada, o processo de construção e exploração web.

