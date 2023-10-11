# Usage de PVOutput
Les données de production sont (Puissance, Energie totale et voltage) envoyées sur la plateforme PVOutput. Si le système est correctement configuré sur cette plateforme, des statistiques intéressantes peuvent être observées.

# Surveillance de panne
Dans le cadre d'une centrale villageoise, la srveillance de panne peut être automatisée. cela fonctionne bien si les instalations sont orientées de manière plus ou moins identiques et dans une zone géographique restreinte. PVOutput propose des APIs. Un des services est [Status-service](https://pvoutput.org/help/api_specification.html#get-status-service).

## Utilisation de l'API PVOutput
Ce point d'API peremet de récupérer un certain nombre de valeurs. Une donnée intéressante est la puissance générée normalisée. C'est la puissance générée à un instant ramenée au kW installé. Les données fournies sont moyennées par tranche de 5 minutes.  
Cet élément permet de déterminer l'état de santé d'une installation en comparant ses données par rapport aux autres installations gérées.

### Mise en place
L'usage du point d'API `getstatus.jsp` permet de récupérer l'historique des valeurs pour une journée donnée. Il est possible de faire jusque 12 appels par heure soit un appel toutes les 5 minutes. Une requête au système permet de récupérer les 13 dernières valeurs. La médiane de la liste donnera la tendance de puissance normalisée.  
La comparaison entre les différents systèmes que vous gérez, s'ils sont cohérents entre eux, permettront de détecter les pannes si une valeur de l'un d'entre eux est inférieure de X%.

`https://pvoutput.org/service/r2/getstatus.jsp?d=<yyyymmdd>&h=1&limit=13` renvoie les valeurs suivantes

````csv
20231011,14:50,14410,3.079,3002,1440,0.308,NaN,NaN,NaN,239.5;20231011,14:45,14290,3.053,3012,3000,0.641,NaN,NaN,NaN,239.8;20231011,14:40,14040,3.000,3029,3120,0.667,NaN,NaN,NaN,238.2;20231011,14:35,13780,2.944,3049,3000,0.641,NaN,NaN,NaN,242.3;20231011,14:30,13530,2.891,3092,3000,0.641,NaN,NaN,NaN,242.9;20231011,14:25,13280,2.838,3114,3120,0.667,NaN,NaN,NaN,242.0;20231011,14:20,13020,2.782,3135,3120,0.667,NaN,NaN,NaN,242.6;20231011,14:15,12760,2.726,3158,3120,0.667,NaN,NaN,NaN,241.7;20231011,14:10,12500,2.671,3171,3120,0.667,NaN,NaN,NaN,241.3;20231011,14:05,12240,2.615,3198,3240,0.692,NaN,NaN,NaN,241.1;20231011,14:00,11970,2.558,3196,3120,0.667,NaN,NaN,NaN,241.2;20231011,13:55,11710,2.502,3211,3240,0.692,NaN,NaN,NaN,238.8;20231011,13:50,11440,2.444,3210,3120,0.667,NaN,NaN,NaN,238.6;20231011,13:45,11180,2.389,3209,3240,0.692,NaN,NaN,NaN,238.9
````
Chaque ligne est séparée par un `;`, chaque valeur est séparée par une `,`. 

