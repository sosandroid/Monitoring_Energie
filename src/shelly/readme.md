
# Shelly devices

Ce script Python connecte un compteur Shelly pro 3EM pour mesurer la quantité d'énergie injectée dans le ballon et couper le routage d'energie en foinction de ce qui a déjà été envoyé dans le ballon d'eau chaude.


## Prérequis
- Python 3.10+
- _optionnel_ compte Emoncms pour sauvegarder les données

## Installation

### Python3
Python est proposé par défaut sur un serveur Ubuntu, veillez à le mettre à jour. Nous avons développé et testé avec une version 3.10
```
sudo apt update
sudo apt -y upgrade
```
Installez `pip`
````
sudo apt install -y python3-pip
````

### Shelly
Copiez le fichier `shelly.py` et `sun2000-sample.conf` dans votre dossier `/home/<user>`

## Le fichier de configuration
La partie général permet de configurer le niveau de débug. A minima, pour commencer le niveau `debug = True` et `senddata = False` permet de s'assurer que les données sont correctement récupérées et mise en forme. 

La partie emoncms se personnalise avec:
- Activation ou non de cette partie
- L'adresse du serveur Emoncms (IP ou nom de domaine, http ou https)
- La clef d'API de votre compte
- Le nom du node sur lequel poster les données

La partie shellypro3em se personnalise avec:
- Activation ou non de cette partie
- L'adresse du serveur Shelly (IP ou nom de domaine, http ou https)

Sauvegardez ce fichier sous le nom `shelly.conf` à coté du script.  
Une fois que tout est OK, passez `senddata = True` puis à `debug = False`


````ini
[general]
#Manage debug level
debug = True
senddata = False

[emoncms]
enabled = True
#set your EmonCMS address, api key, nodename, input labels
url = http://127.0.0.1/input/post
apikey = your-api-key
nodename = your-node-name

[shellypro3em]
enabled = True
url = http://127.0.0.1/
relay_uri = relay/0?turn=
meas1_uri = emeter/0/3em_data
meas2_uri = emeter/1/3em_data
meas3_uri = emeter/2/3em_data

````


## Fonctionnement

### Test
Modifiez les droits pour permettre l'exécution
````
chmod a+x shelly.py
````
Lancez le script
````
python3 ./shelly.py
````
Vous devriez obtenir une réponse comme cella là :
````
{'InstantPower': 0.0, 'InternalTemp': 0.0, 'AllTimeEnergy': 4239.09, 'DailyEnergy': 20.36, 'VoltageL1': 0.0, 'VoltageL2': 0.0, 'VoltageL3': 0.0, 'CurrentL1': 0.0, 'CurrentL2': 0.0, 'CurrentL3': 0.0, 'ActivePower': 0.0, 'GridFrequency': 0.0, 'Efficiency': 0.0, 'DeviceStatusCode': '0xa000'}

Emondata: {'PUI_PROD': 0.0, 'TEMP_INT': 0.0, 'AllTimeEnergy': 4239.09, 'DailyEnergy': 20.36, 'VoltageL1': 0.0, 'VoltageL2': 0.0, 'VoltageL3': 0.0, 'CurrentL1': 0.0, 'CurrentL2': 0.0, 'CurrentL3': 0.0, 'ActivePower': 0.0, 'GridFrequency': 0.0, 'Efficiency': 0.0}

Emon data sent <Response [200]>
````
Elle donne les données lues sur l'onduleur, la mise en forme EmonCMS, le résultat de l'envoi. Si PVOutput et BDPV sont actifs, les données transmises sont également affichées ainsi que le résultat de transmission.  
Vérifiez que les données arrivent correctement sur chaque plateforme. Si c'est OK, il suffit d'automatiser

### Automatisation
Désactivez le mode débug dans le fichier de configuration.  

Vérifiez le chemin complet dans lequel se trouve le script. Comme vu ci-dessous, dans notre cas nous sommes dans `/home/emoncms/onduleur`
```sh
emoncms@emoncms:~/onduleur$ pwd
/home/emoncms/onduleur
```
Créer un fichier `sun2000.sh` dans lequel vous ajoutez les lignes ci-dessous (à adapter). Appelé chaque minute, il lance 4 exécutions séparées de 15 secondes.

````sh
#!/bin/bash
/usr/bin/python3 /home/emoncms/onduleur/sun2000_modbus.py &
sleep 15 && /usr/bin/python3 /home/emoncms/onduleur/sun2000_modbus.py &
sleep 30 && /usr/bin/python3 /home/emoncms/onduleur/sun2000_modbus.py &
sleep 45 && /usr/bin/python3 /home/emoncms/onduleur/sun2000_modbus.py &
````
Rendez le exécutable `chmod a+x sun2000.sh`
Vérifiez le fonctionnement `./sun2000.sh`, 4 jeux de données devraient arriver en 1 minute.

Ajoutez le au crontab `crontab -e`  
`* * * * * /usr/bin/sh /home/emoncms/onduleur/sun2000.sh`

C'est terminé, les données arrivent toutes les 15 secondes.

## A faire
- Améliorer le script en diminuant les appels `Global`
- Mieux utiliser la variable `Config` pour en faire un seul élément


