import requests
import logging
import logging.handlers
from datetime import datetime

datahj = datetime.today()
nmArquivo = str(datahj.strftime("BotTelegram.py - %d_%m_%Y.txt"))
caminhoLog = r'path do log aqui'


log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=caminhoLog+nmArquivo,
                    filemode='w',
                    format=log_format)

def telegram_bot_sendtext(bot_message,file_path):
    try:    
        bot_token = 'seu token aqui'
        bot_chatID = 'id do seu chat'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message

        response = requests.get(send_text)

        body = {
            'chat_id': bot_chatID,
        }
        files = {
            'document': open(file_path, 'rb')
        }
        r = requests.post(f'https://api.telegram.org/bot{bot_token}/sendDocument', data=body, files=files)
        if r.status_code >= 400:
            print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))
        else:
            print('Mensagem enviada com sucesso.')

        return response.json()
    except Exception as e: 
        logging.error(e)

def telegram_bot_sendtext_simple(bot_message):
    try:
        bot_token = 'seu token aqui'
        bot_chatID = 'id do seu chat'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + bot_message

        response = requests.get(send_text)

        return response.json()
    except Exception as e: 
        logging.error(e)