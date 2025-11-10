#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################
# Envoi de mail à travers un SMTP 
#
# V 0.0.1 10/2025 création
# V 0.0.2 11/2025 ajout des certificats SSL explicites
##############################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def envoyer_email_smtp(smtp_conf, liste_destinataires, content):   # Création du message
    
    message = MIMEMultipart('alternative')
    message['From'] = smtp_conf['auth']['user']
    message['To'] = ", ".join(liste_destinataires)  # Liste des destinataires séparés par des virgules
    message['Subject'] = content['sujet']

    #print(message)
    
    # Attachement du corps du message
    
    if 'text' in content:
        message.attach(MIMEText(content['text'], 'plain'))
    if 'html' in content:
        message.attach(MIMEText(content['html'], 'html'))

    try:
        # Connexion au serveur SMTP
        with smtplib.SMTP(smtp_conf['host'], smtp_conf['port']) as serveur:
            if smtp_conf['secure']: 
                serveur.starttls()  # Sécurise la connexion
            serveur.login(smtp_conf['auth']['user'], smtp_conf['auth']['pass'])
            serveur.send_message(message)
        print("E-mail envoyé avec succès à tous les destinataires !")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erreur d'authentification SMTP : {e}")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP : {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
       

