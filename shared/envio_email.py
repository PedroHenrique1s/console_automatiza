import os
from datetime import date
from email.mime.text import MIMEText
import smtplib


def enviar_email(html_body, nome_casa):
    print(f"Preparando e-mail para {nome_casa}...")
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")
    
    destinatarios_raw = os.getenv("EMAIL_DESTINATARIOS")
    if not destinatarios_raw:
        print("Erro: Sem destinatários.")
        return
    lista_para = [email.strip() for email in destinatarios_raw.split(",") if email.strip()]

    copia_raw = os.getenv("EMAIL_COPIA")
    lista_cc = []
    if copia_raw:
        lista_cc = [email.strip() for email in copia_raw.split(",") if email.strip()]

    data_hoje = date.today().strftime("%d/%m/%Y")
    
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = f"Análise de Erro Console - {nome_casa} - {data_hoje}"
    msg['From'] = remetente
    
    msg['To'] = ", ".join(lista_para)
    if lista_cc:
        msg['Cc'] = ", ".join(lista_cc)

    lista_envio_total = lista_para + lista_cc

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, lista_envio_total, msg.as_string())

        print(f"E-mail da {nome_casa} enviado com sucesso!")
        print(f"   Para: {lista_para}")
        print(f"   Cópia: {lista_cc}")

    except Exception as e:
        print(f"Erro SMTP ao enviar {nome_casa}: {e}")