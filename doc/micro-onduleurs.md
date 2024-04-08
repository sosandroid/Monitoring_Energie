# Micro-onduleurs
Quelques liens permettant de récupérer les données des micros-onduleurs et s'inspirer pour adapter les scripts. Ce n'est pas mon installation mais cela peut aider...

## Micro-onduleurs Hoymiles
Le meilleur projet est probablement [OpenDTU](https://www.opendtu.solar). Il permet de s'affranchir du cloud Hoymiles en passant par un clone du DTU. Un autre [projet](https://github.com/wasilukm/hoymiles_modbus) les adresse via modbusTCP

## Micro-onduleur Enphase
Beaucoup de projets pour Enphase afin de lire directement les données Envoy.  Un projet Python [pyEnphase](https://github.com/pyenphase/pyenphase). Il nécessite d'écrire un peu de code pour l'expoloiter. Une autre projet est [Enphase-API](https://github.com/Matthew1471/Enphase-API). Ce projet semble très documenté. Une bonne analyse" de ces deux projets est proposée par [mesgeekeries.ch](https://mesgeekeries.ch/2024/02/03/enphase-demystifier-les-api-locales-avec-des-projets-open-source-en-python/). Les autres projets ci-dessous sont moins aboutis : le travail de [Frédéric Metrich](https://github.com/FredM67/EnvoyS2Emoncms) ou une autre variante le travail de [Markus Fritze](https://github.com/sarnau/EnphaseEnergy).

## Micro-onduleur APSystems
Pour ceux qui veulent se passer du Cloud APSYStems,  un premier moyen [apsystems-qs1-scraper](https://github.com/pdlubisz/apsystems-qs1-scraper) ou [par là](https://github.com/PlanetSmasher/APSystems-ECU-proxy-for-cloudless-operation), plus "extrême" dans la méthode
