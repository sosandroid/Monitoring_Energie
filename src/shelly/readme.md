
# Shelly devices

Ces script Pythons connectent un compteur Shelly pro 3EM pour mesurer la quantité d'énergie injectée dans le ballon et couper le routage d'energie en fonction de ce qui a déjà été envoyé dans le ballon d'eau chaude.

[![Buy me a coffee](../../res/default-yellow.png)](https://www.buymeacoffee.com/ju9hJ8RqGk)

Deux scripts :
- Conenxion en API HTTP Rest
- Connexion en modbus TCP

Le script lodbus est un démonstrateur pour renvoyer les données vers au automate ensuite. Il permet 2 usages : récupération des données en `float` ou en `int`. Certains PLC ne supportant que les valeurs entières. Le script de transmission vers le PLC n'est pas réalisé.


## Prérequis
- Python 3.10+
- compte Emoncms pour sauvegarder les données

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
Copiez le fichier `shelly.py` et `shelly-sample.conf` dans votre dossier `/home/<user>/shelly`

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
Vous devriez obtenir une réponse comme celle là :
````
{"id":0,"a_current":4.029,"a_voltage":236.1,"a_act_power":951.2,"a_aprt_power":951.9,"a_pf":1,"a_freq":50,"b_current":4.027,"b_voltage":236.201,"b_act_power":-951.1,"b_aprt_power":951.8,"b_pf":1,"b_freq":50,"c_current":3.03,"c_voltage":236.402,"c_active_power":715.4,"c_aprt_power":716.2,"c_pf":1,"c_freq":50,"n_current":11.029,"total_current":11.083,"total_act_power":2484.782,"total_aprt_power":2486.7,"user_calibrated_phase":[],"errors":["phase_sequence"]}
````
Elle donne les données lues sur le compteur Shelly, la mise en forme EmonCMS, le résultat de l'envoi. Vérifiez que les données arrivent correctement sur EmonCMS. Si c'est OK, il suffit d'automatiser

### Automatisation
Désactivez le mode débug dans le fichier de configuration.  

Vérifiez le chemin complet dans lequel se trouve le script. Comme vu ci-dessous, dans notre cas nous sommes dans `/home/emoncms/shelly`
```sh
emoncms@emoncms:~/shelly$ pwd
/home/emoncms/shelly
```
Créer un fichier `sun2000.sh` dans lequel vous ajoutez les lignes ci-dessous (à adapter). Appelé chaque minute, il lance 4 exécutions séparées de 15 secondes.

````sh
#!/bin/bash
/usr/bin/python3 /home/emoncms/shelly/shelly.py &
sleep 15 && /usr/bin/python3 /home/emoncms/shelly/shelly.py &
sleep 30 && /usr/bin/python3 /home/emoncms/shelly/shelly.py &
sleep 45 && /usr/bin/python3 /home/emoncms/shelly/shelly.py &
````
Rendez le exécutable `chmod a+x shelly.sh`
Vérifiez le fonctionnement `./shelly.sh`, 4 jeux de données devraient arriver en 1 minute.

Ajoutez le au crontab `crontab -e`  
`* * * * * /usr/bin/sh /home/emoncms/shelly/shelly.sh`

C'est terminé, les données arrivent toutes les 15 secondes.

## A faire
- Améliorer le script en diminuant les appels `Global`
- Mieux utiliser la variable `Config` pour en faire un seul élément





