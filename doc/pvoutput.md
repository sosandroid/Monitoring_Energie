# Usage de PVOutput
Les données de production (Puissance, Energie totale et voltage) sont envoyées sur la plateforme PVOutput. Si le système est correctement configuré sur cette plateforme, des statistiques intéressantes peuvent être récupérées.

# Surveillance de panne
Dans le cadre d'une centrale villageoise, la surveillance de panne peut être automatisée.  
Cela fonctionnera bien si les instalations ont un productible normalisé cohérent et dans une zone géographique restreinte.

## Utilisation de l'API PVOutput
Le point d'API [Status-service](https://pvoutput.org/help/api_specification.html#get-status-service) permet de récupérer la puissance générée normalisée. C'est la puissance générée à un instant ramenée au kW installé. C'est calculé par tranche de 5 minutes. En comparant cette donnée entre les systèmes cohérents entre eux, cela permet de déterminer l'étant de santé d'une installation.

### Mise en place
Le point d'API donne l'historique des valeurs pour une date donnée. Il est possible de faire jusque 12 appels par heure soit un appel toutes les 5 minutes. En travaillant sur l'heure écoulée et la valeur médiane, la puissance générée normalisé sera un bon indicateur. Deux stratégies sont possibles :
- Travailler sur l'écart entre les deux valeurs les plus extrêmes. Cela augmente l'influence de ma météo en micro-local (par exemple nuage à une altitude à 300m, une installation à 450m)
- Travailler sur l'écart à la moyenne ou médianne des médiannes, cela divise par deux l'influence de la météo micro locale

### Traitement des données

`https://pvoutput.org/service/r2/getstatus.jsp?d=<yyyymmdd>&h=1&limit=13` renvoie les valeurs suivantes

````csv
20231011,14:50,14410,3.079,3002,1440,0.308,NaN,NaN,NaN,239.5;20231011,14:45,14290,3.053,3012,3000,0.641,NaN,NaN,NaN,239.8;20231011,14:40,14040,3.000,3029,3120,0.667,NaN,NaN,NaN,238.2;20231011,14:35,13780,2.944,3049,3000,0.641,NaN,NaN,NaN,242.3;20231011,14:30,13530,2.891,3092,3000,0.641,NaN,NaN,NaN,242.9;20231011,14:25,13280,2.838,3114,3120,0.667,NaN,NaN,NaN,242.0;20231011,14:20,13020,2.782,3135,3120,0.667,NaN,NaN,NaN,242.6;20231011,14:15,12760,2.726,3158,3120,0.667,NaN,NaN,NaN,241.7;20231011,14:10,12500,2.671,3171,3120,0.667,NaN,NaN,NaN,241.3;20231011,14:05,12240,2.615,3198,3240,0.692,NaN,NaN,NaN,241.1;20231011,14:00,11970,2.558,3196,3120,0.667,NaN,NaN,NaN,241.2;20231011,13:55,11710,2.502,3211,3240,0.692,NaN,NaN,NaN,238.8;20231011,13:50,11440,2.444,3210,3120,0.667,NaN,NaN,NaN,238.6;20231011,13:45,11180,2.389,3209,3240,0.692,NaN,NaN,NaN,238.9
````
Chaque ligne est séparée par un `;`, chaque valeur est séparée par une `,`. 

````python
normalizedPower = {}
data = '20231011,14:50,14410,3.079,3002,1440,0.308,NaN,NaN,NaN,239.5;20231011,14:45,14290,3.053,3012,3000,0.641,NaN,NaN,NaN,239.8;20231011,14:40,14040,3.000,3029,3120,0.667,NaN,NaN,NaN,238.2'
lines = data.split(';')
for line in lines:
    row = line.split(',')
    normalizedPower[] = row[6]
````

