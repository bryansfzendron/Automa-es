from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import logging.handlers
from time import sleep
import requests
import logging
from BotTelegram import telegram_bot_sendtext_simple

datahj = datetime.today()
dataArquivo = str(datahj.strftime("%d-%m-%Y"))
nmArquivo = str(datahj.strftime("apiDeployPipe.py - %d_%m_%Y.txt"))
DataEmail = str(datahj.strftime("%d/%m/%Y - %H:%M:%S"))
caminhoLog = r'caminho do log'
c = 0
pipelines = list()
erros = list()
namepipelines = list()
url = 'https://learn.microsoft.com/en-us/rest/api/power-bi/pipelines/get-pipelines#code-try-0'
Usuario = 'email da microsoft'
Senha = 'senha'

#configurações referente ao log
log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=caminhoLog+nmArquivo,
                    filemode='w',
                    format=log_format)

# função para pegar o token de acesso da api
def pegartoken():
    try:
        options = Options()
        options.headless = True
        navegador = webdriver.Firefox(options=options)
        print('firefox headless')
        navegador.get(url)
    except Exception as e: 
        logging.error(e)
        telegram_bot_sendtext_simple(bot_message='apiDeployPipe.py - '+str(e))
        navegador.quit()
        pegartoken()
        
    try:
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, 'try-it-sign-in')))
        sleep(1)
        navegador.find_element(By.ID, 'try-it-sign-in').click()
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]')))
        sleep(1)
        navegador.find_element(By.XPATH,'/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]').send_keys(Usuario + Keys.RETURN)
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div/div/div[2]')))
        sleep(1)
        navegador.find_element(By.CLASS_NAME, 'table-cell').click()
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.NAME, 'passwd')))
        sleep(1)
        navegador.find_element(By.NAME, 'passwd').send_keys(Senha + Keys.RETURN) 
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input')))
        sleep(1)
        navegador.find_element(By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input').click()
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.ID, 'continue-with-account')))
        sleep(1)
        navegador.find_element(By.ID, 'continue-with-account').click()
        sleep(1)
        element = WebDriverWait(navegador, 20).until(EC.presence_of_element_located((By.NAME, 'http-request')))
        sleep(1)
        elemento = navegador.find_element(By.XPATH,'/html/body/div[3]/div/form/div[2]/div[4]/pre/span').text
        elemento = elemento.split(' ')
        token = elemento[3]
        navegador.quit()
    except Exception as e: 
        logging.error(e)    
        telegram_bot_sendtext_simple(bot_message='apiDeployPipe.py - '+str(e))
        navegador.quit()
        pegartoken()
    return token

token = pegartoken()

print(token)  
headers = { 
    'Authorization': f'Bearer {token}'
}
json_data = {
  "sourceStageOrder": 0,
  "options": {
    "allowOverwriteArtifact": True,
    "allowCreateArtifact": True
  }
}

try:
    response = requests.get('https://api.powerbi.com/v1.0/myorg/pipelines',headers=headers).json()
    print(response)
except Exception as e:
    logging.error(e)    
    telegram_bot_sendtext_simple(bot_message='apiDeployPipe.py - '+str(e))
try:
    while True:
        pipelines.append(response['value'][c]['id'])
        namepipelines.append(response['value'][c]['displayName'])
        c+=1
    
except:
    print(namepipelines)
    print('Final da lista')

try:
    for pipeline in pipelines:
        response = requests.post(f'https://api.powerbi.com/v1.0/myorg/pipelines/{pipeline}/deployAll', headers=headers, json=json_data)
        responseP = response.json()
        sleep(1)
        print(pipeline,"Atualizado")
        if responseP['status'] == 'Failed':
            erros.append([pipeline,responseP['status']])
            erros = str(erros).strip('[]')
    erros = str(erros).strip('[]')
    if len(erros)>0:
        telegram_bot_sendtext_simple(bot_message='apiDeployPipe.py - '+str(erros))
except Exception as e:
    logging.error(e)
    telegram_bot_sendtext_simple(bot_message='apiDeployPipe.py - '+str(e))

        




