import requests
import json
import os 
import logging.handlers
import logging
from datetime import datetime
import sys

sys.path.append(r'PATH DAS CLASSES IMPORTADAS')

#import do bot de avisos do log de erro
from BotTelegram import telegram_bot_sendtext_simple

datahj = datetime.today()
nmArquivo = str(datahj.strftime("bottelegram.py - %d_%m_%Y.txt"))
caminhoLog = r'SEU PATH PARA O LOG AQUI'

# DEFINE FORMATO E CONFIGURAÇÕES DO ARQUIVO DE LOG
log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=caminhoLog+nmArquivo,
                    filemode='w',
                    format=log_format)



class TelegramBot:
    def __init__(self):
       token = 'SEU TOKEN AQUI'
       self.url_base = f'https://api.telegram.org/bot{token}/'
    # Iniciar o Bot
    def Iniciar(self):
        update_id=None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            mensagens = atualizacao['result']
            print(mensagens)
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    self.chat_id = mensagem['message']['from']['id']
                    eh_primeira_mensagem = mensagem['message']['message_id'] == 1
                    resposta = self.criar_resposta(mensagem,eh_primeira_mensagem)
                    self.responder(resposta,self.chat_id)
                

    def obter_mensagens(self,update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def criar_resposta(self,mensagem,eh_primeira_mensagem):
        mensagem = mensagem['message']['text']
        if eh_primeira_mensagem == True or mensagem == "menu" or mensagem not in ('0','1'):
            return f'''Qual é numero da solicitação?{os.linesep}1 - Relatório de Pendências (SMDS){os.linesep}0 - sair'''
        
        
        token = '5826567171:AAF9gjYj_V-jCmzNmMUVqWtUoz4nv6F4HWM'
        if mensagem == '1':
            body = {
                'chat_id': self.chat_id
            }
            caminho = r'D:\Gdrive\Dados_Publicos_SP\python\Relatorios\ProjetoCrescer\Pendencias\\'
            file_path=self.ultimoArquivo(caminho)
            files = {
                'document': open(file_path, 'rb')
            }
            r = requests.post(f'https://api.telegram.org/bot{token}/sendDocument', data=body, files=files)
            if r.status_code >= 400:
                print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))
            else:
                return('')
        elif mensagem == '0':
            return ('Até logo')
        else:
            return 'Gostaria de acessar o menu? Digite "menu"'

    def responder(self,resposta,chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)

#PEGA O ULTIMO ARQUIVO INSERIDO NA PASTA
    def ultimoArquivo(self,caminho):
        caminhoDir =  [os.path.join(caminho, nome) for nome in os.listdir(caminho)]
        caminhoUstr = max(caminhoDir, key=os.path.getctime) 
        return caminhoUstr
try:
    if __name__ =="__main__":
        bot = TelegramBot()
        bot.Iniciar()
except Exception as e: 
    logging.error(e)
    telegram_bot_sendtext_simple(bot_message='BotTelegram-Replit.py - '+str(e))
    bot = TelegramBot()
    bot.Iniciar()  
