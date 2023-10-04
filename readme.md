# Monitoring d'energie panneaux photovoltaïques et Linky

L'objectif est de surveiller une installation photovolatïque en auto-consommation individuelle. Nous avons donc 3 données à surveiller et à mettre en forme pour avoir un graphique de ce type :
- Puissance soutirée du réseau
- Puissance injectée dans le réseau
- Puissance produite par les panneaux

Ce repo est autant un partage qu'un aide mémoire.

![Profil Consommation](./res/Auto-conso-solaire.jpg)

## Système mis en place
La récolte de données se fait via un [Denky D4](https://github.com/hallard/Denky-D4) basé sur un ESP32, proposé par Charles Hallard. Il récolte les puissances importées et exportées sur le Linky. Il est secondé par [EmonCMS](https://github.com/emoncms/emoncms) qui se charge d'aggréger et présenter les données. L'onduleur livre, lui, ses données via un script Python sur mesure. Les données de production sont également envoyées sur [PVOutput.org](https://pvoutput.org)

```mermaid
flowchart LR;
    A(Linky)-->B;
    B(Denky D4)--PUI_SOUT & PUI_INJ-->C;
    C([EmonCMS])-->D;
    D([SolarPV App]);
    E(Onduleur Sun2000)-->F;
    F([sun2000_modbus.py])--PUI_PROD-->C
    F--PUI_PROD & Total_Energy-->G([PVOutput.org])
```
## EmonCMS
Installé sur un serveur local [Ubuntu Server](https://ubuntu.com/download/server) 22.04 LTS. L'installation depuis une clef "Live-usb" se fait facilement. Voir [là](https://doc.ubuntu-fr.org/live_usb) et [là](https://doc.ubuntu-fr.org/tutoriel/installation_sur_disque_usb).  
Le [tutoriel](https://github.com/openenergymonitor/EmonScripts/blob/master/docs/install.md) openEnergyMonitor est à suivre à la lettre pour EmonCMS. Il permet d'arriver au bout de l'installation sans éccueil. J'ai ajouté ensuite Python3 et pyModbus.

Dès que les données arrivent, elles sont disponibles dans "Inputs" et il s'agit d'en faire des "Feeds". Ce sont les feeds qui alimentent les dashboards. C'est parfaitement expliqué sur la doc de [SolarPV](https://docs.openenergymonitor.org/applications/solar-pv.html#configure-feeds).

## Denky D4
Matériel plutôt simple, il arrive prêt à fonctionner. Une [mise à jour](https://github.com/hallard/Denky-D4#firmware) plus tard, il est opérationnel. Le [tutoriel](https://github.com/hallard/Denky-D4#tasmota-template) proposé permet d'activer le template Tasmota adéquat et d'ajouter le Berry Script qui transfère les données, dont nous avons besoin, vers EmonCMS. Mon [script](./src/denky.be) est proposé pour illustration. Il envoie toutes les 15 secondes les données lues sur le Linky.

Selon le mode de communication du Linky, il faudra activer le mode standard (9600 bauds) ou le mode historique (1200 bauds). Voir la [doc](https://tasmota.github.io/docs/Teleinfo/#configuring-teleinfo).   
En mode standard, la commande est `energyconfig standard`, en mode historique, la commande est `energyconfig historique`.  
La liste des étiquettes TIC fournie, pour mémoire, [Standard](./tic_standard.md) et [Historique](tic_historique.md). Il est à remarquer que pour de l'autoconsommation, le mode standard est nécessaire.

__Remarque__ : l'interface proposée par le Denky n'est pas conçue pour un mode en autoconsommation. Les données remontées peuvent être _bizarres_ en apparence. Il remonte néanmoins correctement les données lues du Linky vers EmonCMS. Rien de grave, c'est juste à garder en tête.

![denky d4](./res/denky.jpg "affichage pendant export").

## L'onduleur Huawei
L'onduleur Sun2000 de Huawei propose une interface ModbusTCP. Il faut l'activer depuis l'application FusionSolar pour qu'elle soit accessible par tous. 
Le [script](./src/sun2000_modbus) proposé connecte l'onduleur et les récupère pour les envoyer sur EmonCMS et/ou PVOutput. Le fichier de configuration permet de personnaliser à votre installation.  
La [doc Huawei](./res/Huawei-Modbus) et [ModbusTool](https://github.com/ClassicDIY/ModbusTool) a bien servi pour vérifier la lecture correcte des données via le script Python.

L'installation est décrite via le fichier [markdown](./src/sun2000_modbus/sun2000_modbus.md)

---
Pour les autres types d'installation sur microonduleur, pour ceux qui me l'on demandé. Il faut s'inspirer des éléments ci-dessous.
## Micro-onduleur Enphase
Ce n'est pas mon installation, mais cela peut aider. Pour lire de manière directe les données de la passerelle Enphase, le travail de [Frédéric Metrich](https://github.com/FredM67/EnvoyS2Emoncms) est assez intéressant. Une autre variante est d'utiliser le travail de [Markus Fritze](https://github.com/sarnau/EnphaseEnergy).

## Micro-onduleur APSystems
Pour ceux qui veulent se passer du Cloud APSYStems,  un premier moyen [apsystems-qs1-scraper](https://github.com/pdlubisz/apsystems-qs1-scraper) ou [par là](https://github.com/PlanetSmasher/APSystems-ECU-proxy-for-cloudless-operation), plus "extrême" dans la méthode

## Micro-onduleurs Hoymiles
Un [projet](https://github.com/wasilukm/hoymiles_modbus) les adresse via modbusTCP
