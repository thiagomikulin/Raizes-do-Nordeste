import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PW = os.getenv("EMAIL_PW")



def solicitar_reset_senha(email):
    enviador = str(EMAIL_HOST)
    senha = str(EMAIL_PW)
    assunto = 'Troca de senha'
    corpo = f'''
    Olá! Tudo bem?
    Este é um e-mail automático da rede Raízes do Nordeste!

    Recebemos uma solicitação de troca de e-mail para o seu email. 
    Caso você não tenha solicitado, favor desconsiderar a mensagem
    Se você solicitou a troca, clique [aqui] aqui para alterar sua senha
    '''

    mensagem = MIMEMultipart()
    mensagem['From'] = enviador
    mensagem['To'] = email
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        print('teste')
        servidor.starttls()
        servidor.login(enviador, senha)
        servidor.send_message(mensagem)
    return {
            "message":"Email de troca de senha enviado com sucesso!",
            "email":email
    }

def trocar_senha(email):
        pass