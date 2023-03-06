import telebot
from telegram.constants import ParseMode
import requests
import json
import os 
import logging.handlers
import logging
from datetime import datetime
import sys
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re 
sys.path.append(r'D:\Gdrive\Dados_Publicos_SP\python\GabineteEstrategico')
from BotTelegram import telegram_bot_sendtext_simple


datahj = datetime.now()
nmArquivo = str(datahj.strftime("MandaEmail.py - %d_%m_%Y.txt"))
caminhoLog = r'path do log'
curriculo = r'path do curriculo'
GMAIL_ID = 'email gmail'
GMAIL_PWD = 'senha de app configurada no gmail'

CHAVE_API = "token do telegram"

bot = telebot.TeleBot(CHAVE_API)

def iniciar ():
    @bot.message_handler(commands=["start"])
    def opcaoStart(mensagem):
        bot.send_message(mensagem.chat.id, 
                    text='''Olá meu nome é Bryan Zendron, este é meu chatBot Currículo interaja com ele para descobrir mais sobre minha trajetória profissional. O que você gostaria de saber sobre mim:

*/1. Formação 👨‍🎓
/2. Idiomas 🌎
/3. Domínio em tecnologia 👨‍💻
/4. Certificações 📚
/5. Download Currículo PDF ⬇️
/6. Mande uma mensagem no meu e-mail por aqui ! 📩*
''', 
                    parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["1"])
    def opcao1(mensagem):
        texto = '''👨‍🎓 *Formação Acadêmica:* 

Bacharel em Ciência da Computação
Universidade Paulista - UNIP, Santana de Parnaíba
01/2018 – 01/2022

Pós Graduação em Inteligência Artificial e Machine Learning
Universidade Cruzeiro do Sul.
06/2022 – 06/2023
'''
        bot.send_message(mensagem.chat.id, texto,parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["2"])
    def opcao2(mensagem):
        texto = '''🌎 *Idiomas:*

Portugês 🇧🇷: Nativo  
Espanhol 🇪🇸: Técnico'''
        bot.send_message(mensagem.chat.id, texto,parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["3"])
    def opcao3(mensagem):
        texto = '''*👨‍💻 As tecnologias que eu conheço até o momento são:*
                
- Microsoft Power BI
- Python
- Microsoft SQL Server
- HTML 
- CSS
- Excel Avançado'''
        bot.send_message(mensagem.chat.id, texto,parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["4"])
    def opcao4(mensagem):
        texto = '''*📚 As certificações que possuo até o momento são:*

- PL300 - Power BI Data Analyst Associate Microsoft – 12/2022
- Master Power BI – De A à Z – 09/2021
- Power BI Intermediário – 09/2021
- Power BI DAX II Avançado – 07/2022
- Power BI DAX III Avançado e DAX Studio – 07/2022
- Python Linguagem de Programação – 05/2022
- PYTHON 3 - MUNDO 1 – 05/2022
- PYTHON 3 - MUNDO 2 – 05/2022'''
        bot.send_message(mensagem.chat.id, texto,parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["5"])
    def opcao5(mensagem):
        pdf_doc = open(curriculo, 'rb')
        bot.send_message(mensagem.chat.id, "🧾 *Curriculo:*",parse_mode=ParseMode.MARKDOWN)
        bot.send_document(mensagem.from_user.id, pdf_doc)

    @bot.message_handler(commands=["6"])
    def opcao6(mensagem):
        bot.send_message(mensagem.chat.id, "Vou precisar de algumas informaçoes clique /Sim para continuar.",parse_mode=ParseMode.MARKDOWN)

    @bot.message_handler(commands=["Sim"])
    def opcaoSim(mensagem):
        digiteEmail  = bot.send_message(mensagem.chat.id, "Digite o seu Email:",parse_mode=ParseMode.MARKDOWN)
        bot.register_next_step_handler(digiteEmail, Email)
        
    def Email(pm):
        email = pm.text.lower()
        if check(email=email) == False:
            bot.send_message(pm.chat.id,text='O e-mail digitado é invalido!')
            digiteEmail =  bot.send_message(pm.chat.id,text='Digite um e-mail valido por favor')
            bot.register_next_step_handler(digiteEmail, Email)
        else:
            sent_msg = bot.send_message(pm.chat.id, f"O que você gostaria de mandar?")
            bot.register_next_step_handler(sent_msg, corpoEmail, email) #Next message will call the age_handler function

    def corpoEmail(pm, email):
        corpo = pm.text
        try:
            if __name__ =="__main__":
                enviaEmailSimples(corpo=f'Usuário: {email}\nMensagem: {corpo}')
                bot.send_message(pm.chat.id, f"Email enviado com Sucesso!.")
                
        except Exception as e: 
            bot.send_message(pm.chat.id, f"Erro ao enviar e-mail, tente novamente mais tarde!")
            logging.error(e)
            telegram_bot_sendtext_simple(bot_message='BotTelegram-Replit.py - '+str(e))


    def verificar(mensagem):
        return True

    @bot.message_handler(func=verificar)
    def responder(mensagem):
        bot.send_message(mensagem.chat.id, 
                    text='''Olá meu nome é Bryan Zendron, este é meu chatBot Currículo interaja com ele para descobrir mais sobre minha trajetória profissional. O que você gostaria de saber sobre mim:

*/1. Formação 👨‍🎓
/2. Idiomas 🌎
/3. Domínio em tecnologia 👨‍💻
/4. Certificações 📚
/5. Download Currículo PDF ⬇️
/6. Mande uma mensagem no meu e-mail por aqui ! 📩*
''', 
                    parse_mode=ParseMode.MARKDOWN)


    def enviaEmailSimples(corpo):
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)   
        server.login(GMAIL_ID, GMAIL_PWD)  
        enviarEmail = MIMEMultipart()
        enviarEmail['From'] = GMAIL_ID
        enviarEmail['to'] = 'bryan.zendron@gmail.com' 
        enviarEmail['subject'] = 'Currículo Chat Bot'
        enviarEmail.attach(MIMEText(corpo, 'plain'))
        server.sendmail(enviarEmail["From"], enviarEmail["To"].split(";"), enviarEmail.as_string())
        server.quit()

#checa se o email digitado tem o padrão de email.
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    def check(email):  
        if(re.search(regex,email)):  
            checkEmail = True  
            
        else:
            checkEmail = False 
        return checkEmail
        
            

    bot.polling()

try:
    if __name__ =="__main__":
        iniciar()
except Exception as e: 
    logging.error(e)
    telegram_bot_sendtext_simple(bot_message='BotTelegram-Replit.py - '+str(e))
    iniciar()

