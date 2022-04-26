import platform
import subprocess
import smtplib
from email.message import EmailMessage
from secret import senha
import urllib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

server1 = '192.168.1.200'
server2 = '192.168.0.120'
server3 = '192.168.1.100'


def myping(host):
    parameter = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parameter, '1', host]
    response = subprocess.call(command)

    if response == 0:
        print('servidor ligado')
    else:
        print('erro')
        # Configurar email e senha
        EMAIL_ADDRESS = 'yashimarured@gmail.com'
        EMAIL_PASSWORD = senha

        # Criar um e-mail
        msg = EmailMessage()
        msg['Subject'] = 'Monitoramento Servidor'
        msg['From'] = 'yashimarured@gmail.com'
        msg['To'] = 'guilhermeh.jesus@hotmail.com'
        msg.set_content('Servidor Desligado, favor verificar ...')

        # Enviar um email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print('mensagem enviada')
            whatsapp()


def whatsapp():
    # WhatsApp

    contatos_df = pd.read_excel("pythoncel.xlsx")
    print("passou")
    navegador = webdriver.Chrome()
    print("passou")
    navegador.get("https://web.whatsapp.com/")
    print("passou")

    while len(navegador.find_elements_by_id("side")) < 1:
        time.sleep(30)

    # Login já efetuado no Whatsapp
    for i, mensagem in enumerate(contatos_df['Mensagem']):
        pessoa = contatos_df.loc[i, "Pessoa"]
        numero = contatos_df.loc[i, "Numero"]
        texto = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
        navegador.get(link)
        while len(navegador.find_elements_by_id("side")) < 1:
            time.sleep(30)

    navegador.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
    


running = myping(server2)
del running
