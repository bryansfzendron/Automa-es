from time import sleep
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from datetime import date
from dateutil.relativedelta import relativedelta



MesAnterior = date.today() + relativedelta(months=-1)
ano = MesAnterior.year


#Xpath Elementos
tabelaChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[2]/div/div[1]/div/table'
anoChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select'
regiaoChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[2]/div/select'
MunicipiosChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[3]/div[1]/div/select'
produtividadepolicialChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[5]/div[2]/div/a '
ocorrenciasChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[5]/div[1]/div/a'
RegiaoChrome = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[2]/div/select'

#Variaveis 
caminhoProdPolicia = r'caminho da pasta de produtividade policial'
caminhoDelitos = r"caminho da pasta de delitos"
Caminho = r'Caminho da pasta para baixar arquivos'
url = 'https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx'
Municipios = ("Americana", "Araçatuba", "Araraquara", "Araras", "Assis", "Atibaia", "Barretos", "Barueri", "Bauru", "Birigui", "Botucatu", "Bragança Paulista", "Caieiras", "Caraguatatuba", "Carapicuíba", "Catanduva", "Cotia", "Cubatão", "Diadema", "Embu das Artes", "Ferraz de Vasconcelos", "Franca", "Francisco Morato", "Franco da Rocha", "Guaratinguetá", "Guarujá", "Hortolândia", "Indaiatuba", "Itanhaém", "Itapecerica da Serra", "Itapetininga", "Itapevi", "Itaquaquecetuba", "Itatiba", "Itu", "Jacareí", "Jandira", "Jaú", "Jundiaí", "Leme", "Limeira", "Mairiporã", "Marília", "Mauá", "Mogi das Cruzes", "Mogi Guaçu", "Ourinhos", "Paulínia", "Pindamonhangaba", "Piracicaba", "Poá", "Praia Grande", "Presidente Prudente", "Ribeirão Pires", "Rio Claro", "Salto", "Santa Bárbara d'Oeste", "Santana de Parnaíba", "Santos", "São Caetano do Sul", "São Carlos", "São José do Rio Preto", "São Vicente", "Sertãozinho", "Sumaré", "Suzano", "Taboão da Serra", "Tatuí", "Taubaté", "Valinhos", "Várzea Paulista", "Votorantim", "Osasco", "Cajamar", "São Bernardo do Campo", "Santo André", "Guarulhos", "São Paulo")


#aguarda o downloads terminar antes de executar qualquer função.
def download_wait(caminho, timeout, nfiles=None):
   
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        sleep(1)
        dl_wait = False
        files = os.listdir(caminho)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds

#pega o ultimo arquivo inserido na pasta
def ultimoArquivo(caminho):
    caminhoDir =  [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
    caminhoUstr = max(caminhoDir, key=os.path.getctime) 
    return caminhoUstr


chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs', {
"plugins.always_open_pdf_externally": True,"download.default_directory" : Caminho,})
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)
sleep(1)


#Ocorrências Mensais Estado
for Municipio in Municipios:
    nomeArquivo2 = f'Estado de São Paulo-{ano}.csv'
    nomeArquivoProd = f'Estado de São Paulo-{ano}.csv'
    driver.find_element(By.XPATH,regiaoChrome).send_keys('Todos')
    driver.find_element(By.XPATH,anoChrome).send_keys(ano)
    driver.find_element(By.XPATH,MunicipiosChrome).send_keys(Municipio)
    driver.find_element(By.XPATH,ocorrenciasChrome).click()
    Tabela = driver.find_element(By.XPATH,tabelaChrome)
    dados = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[1]/form/div[3]/div[2]/div/div[1]')
    html = dados.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table")
    line = []
    data = [d for d in table.select("th")]
    print(data)
    for d in data:
        linha = ""
        linha += d.text+","   
        line.append(linha)
    line_even = []
    data = [ d for d in table.select("tr")]
    for d in data:
        linha = ""
        for t in d.select("td"):
            linha += t.text+","
        line_even.append(linha)
    with open(f'{caminhoDelitos} Município {Municipio}-{ano}.csv', "w") as f:
        f.write(''.join(line))
        for l in line_even:
            f.write(l+"\n")

#Produtividade Policial
for Municipio in Municipios:

    nomeArquivo2 = f'Estado de São Paulo-{ano}.csv'
    nomeArquivoProd = f'Estado de São Paulo-{ano}.csv'
    driver.find_element(By.XPATH,regiaoChrome).send_keys('Todos')
    driver.find_element(By.XPATH,anoChrome).send_keys(ano)
    driver.find_element(By.XPATH,MunicipiosChrome).send_keys(Municipio)
    driver.find_element(By.XPATH,produtividadepolicialChrome).click()
    Tabela = driver.find_element(By.XPATH,tabelaChrome)
    dados = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[1]/form/div[3]/div[2]/div/div[1]')
    html = dados.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table")
    line = []
    data = [d for d in table.select("th")]
    for d in data:
        linha = ""
        linha += d.text+","   
        line.append(linha)
    line_even = []
    data = [ d for d in table.select("tr")]
    for d in data:
        linha = ""
        for t in d.select("td"):
            linha += t.text+","
        line_even.append(linha)
    with open(f'{caminhoProdPolicia} ProdutividadePolicial-Município {Municipio}-{ano}.csv', "w") as f:
        f.write(''.join(line))
        for l in line_even:
            f.write(l+"\n")

driver.quit()


