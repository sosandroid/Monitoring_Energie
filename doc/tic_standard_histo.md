# TIC Mode Standard et historique

## Liste des étiquettes
Tentative d'équivalence entre les étiquettes des deux modes. Voir les documents de référence [Enedis-NOI-CPT_54E.pdf](./Enedis-NOI-CPT_54E.pdf) et [Enedis-NOI-CPT_02E.pdf](./Enedis-NOI-CPT_02E.pdf)

|Etiquette Standard | Description | Etiquette Historique |
|--|--|--|
|ADSC | Adresse secondaire du compteur| ADCO |
|VTIC | Version de la TIC| - |
|DATE | Date et heure courante| - |
|NGTF | Nom du calendrier tarifaire fournisseur| OPTARIF |
| - | Horaire heure pleine, heure creuse _(équivalent à LTARF ?)_ | HHPHC |
|LTARF | Libellé tarif fournisseur en cours| PTEC |
|EAST | Energie active soutirée totale| BASE |
|EASF01 | Energie active soutirée Fournisseur index 01| BASE <br> HCHC <br> EJPHN <br> BBRHCJB |
|EASF02 | Energie active soutirée Fournisseur index 02| HPHP <br> EJPHPM <br> BBRHPJB |
|EASF03 | Energie active soutirée Fournisseur index 03| BBRHCJW |
|EASF04 | Energie active soutirée Fournisseur index 04| BBRHPJW |
|EASF05 | Energie active soutirée Fournisseur index 05| BBRHCJR |
|EASF06 | Energie active soutirée Fournisseur index 06| BBRHPJR |
|EASF07 | Energie active soutirée Fournisseur index 07| - |
|EASF08 | Energie active soutirée Fournisseur index 08| - |
|EASF09 | Energie active soutirée Fournisseur index 09| - |
|EASF10 | Energie active soutirée Fournisseur index 10| - |
|EASD01 | Energie active soutirée Distributeur index 01| - |
|EASD02 | Energie active soutirée Distributeur index 02| - |
|EASD03 | Energie active soutirée Distributeur index 03| - |
|EASD04 | Energie active soutirée Distributeur index 04| - |
|EAIT | Energie active injectée totale| - |
|ERQ1 | Energie réactive Q1 totale| - |
|ERQ2 | Energie réactive Q2 totale| - |
|ERQ3 | Energie réactive Q3 totale| - |
|ERQ4 | Energie réactive Q4 totale| - |
|IRMS1 | Courant efficace phase 1| IINST <br> IINST1 |
|IRMS2 | Courant efficace phase 2| IINST2 |
|IRMS3 | Courant efficace phase 3| IINST3 |
| - | Courant max phase 1 | IMAX1 |
| - | Courant max phase 2 | IMAX2 |
| - | Courant max phase 3 | IMAX3 |
|URMS1 | Tension efficace phase 1| - |
|URMS2 | Tension efficace phase 2| - |
|URMS3 | Tension efficace phase 3| - |
|PREF | Puissance app. de référence| _Voir ISOUSC_ |
|PCOUP | Puissance app. de coupure| - |
|SINSTS | Puissance app. Instantanée soutirée| PAPP |
|SINSTS1 | Puissance app. Instantanée soutirée phase 1| - |
|SINSTS2 | Puissance app. Instantanée soutirée phase 2| - |
|SINSTS3 | Puissance app. Instantanée soutirée phase 3| - |
|SMAXSN | Puissance app. max. soutirée n|
|SMAXSN1 | Puissance app. max. soutirée n phase 1|
|SMAXSN2 | Puissance app. max. soutirée n phase 2|
|SMAXSN3 | Puissance app. max. soutirée n phase 3|
|SMAXSN-1 | Puissance app max. soutirée n-1| PMAX |
|SMAXSN1-1 | Puissance app max. soutirée n-1 phase 1|
|SMAXSN2-1 | Puissance app max. soutirée n-1 phase 2|
|SMAXSN3-1 | Puissance app max. soutirée n-1 phase 3|
|SINSTI | Puissance app. Instantanée injectée | - |
|SMAXIN | Puissance app. max. injectée n | - |
|SMAXIN-1 | Puissance app max. injectée n-1 | - |
|CCASN | Point n de la courbe de charge active soutirée| - |
|CCASN-1 | Point n-1 de la courbe de charge active soutirée| - |
|CCAIN | Point n de la courbe de charge active injectée| - |
|CCAIN-1 | Point n-1 de la courbe de charge active injectée| - |
|UMOY1 | Tension moy. ph. 1| - |
|UMOY2 | Tension moy. ph. 2| - |
|UMOY3 | Tension moy. ph. 3| - |
|STGE | Registre de Statuts| - |
|DPM1 | Début Pointe Mobile 1| - |
|FPM1 | Fin Pointe Mobile 1| - |
|DPM2 | Début Pointe Mobile 2| - |
|FPM2 | Fin Pointe Mobile 2| - |
|DPM3 | Début Pointe Mobile 3| - |
|FPM3 | Fin Pointe Mobile 3| - |
|MSG1 | Message court| - |
|MSG2 | Message ultra court| - |
|PRM | PRM| - |
|RELAIS | Relais| - |
|NTARF | Numéro de l’index tarifaire en cours| - |
|NJOURF | Numéro du jour en cours calendrier fournisseur| - |
|NJOURF+1 | Numéro du prochain jour calendrier fournisseur| - |
|PJOURF+1 | Profil du prochain jour calendrier fournisseur| - |
|PPOINTE | Profil du prochain jour de pointe|
| - | Préavis début EJP (30 min) | PEJP |
| _voir le contenu de STGE et son décodage_ | Couleur du lendemain (BLEU, BLAN, ROUG) | DEMAIN |
| _voir PREF_ | Intenisté souscrite (PREF en VA / 200V) en monophasé <br> Intensité souscrite (PREF en VA / 200V)/3 en triphasé | ISOUSC |
| - | Avertissement dépassement puissance souscrite | ADPS |
| - | Avertissement dépassement intenisté phase 1 | ADIR1 |
| - | Avertissement dépassement intenisté phase 2 | ADIR2 |
| - | Avertissement dépassement intenisté phase 3 | ADIR3 |
| - | Présence des potentiels | PPOT |
| - | Mot d'état du compteur - usage réservé au distributeur, non documenté | MOTDETAT |

## Décodage ADSC / ADC0
ADSC d'exemple 012361456789 pour un **Linky**

|01|23|61|456789|
|--|--|--|--|
|Code constructeur|Millesime de production|**61** mono 60A G3<br> **6**2 mono 90A G1 <br> **63** tri 60A G1 <br> **64** mono 60A G3 <br> **70** mono 60A G3 <br> **71** tri 60A G3 <br> **75** mono 90A G3 <br> **76** tri 60A G3|Matricule du compteur|

## Décodage STEG
Registre des statuts pour le mode standard. Composé de 4 octets exprimé en hexadécimal

| Octet 4 | Octet 3 | Octet 2 | Octet 1 |
|---|---|---|---|

**Octet 1**
|7|6|5|4|3..1|0|
|---|---|---|---|---|---|
| Dépassement puissance <br> 0: Pas de dépassement <br> 1: dépassement en cours | Surtension sur une phase <br> 0: Pas de surtension <br> 1: surtension sur au moins une phase, peut provoquer une alarme pour concentrateur (voir registre _alarmfilter_) | Non utilisé: 0 | Cache borne distributeur <br> 0: fermé <br> 1: ouvert | organe de coupure<br>0: fermé <br> 1: ouvert sur surpuissance <br> 2: ouvert sur surtension <br> 3: ouvert sur délestage <br> 4: ouvert sur ordre CPL ou Euridis <br >5: ouvert sur surchauffe avec courant supérieur au courant de commutation max <br >6: ouvert sur surchauffe avec courant inférieur au courant de commutation max | Contact sec <br> 0: ouvert <br> 1: fermé |
| (X & 0x80) >> 7 | (X & 0x40) >> 6 | (X & 0x20) >> 5 | (X & 0x10) >> 4 | (X & 0x0E) >> 1 | (X & 0x01) |

**Octet 2**
|15..14|13..10|9|8|
|---|---|---|---|
| tarif en cours sur contrat distributeur _(EASDxx)_ <br> 0: vers index 1 <br> 1: vers index 2 <br> 2: vers index 3 <br> 3: vers index 4 | Tarif en cours sur constrat fourniture _(EASFxx)_  <br> 0: vers index 1 <br> 1: vers index 2 <br> 2: vers index 3 <br> 3: vers index 4 <br> 4: vers index 5 <br> 5: vers index 6 <br> 6: vers index 7 <br> 7: vers index 8 <br> 8: vers index 9 <br> 9: vers index 10 | Sens de l'énergie active <br> 0: Energie active positive (consommation) <br> 1: énergie active négative (production) | Fonctionnement <br> 0:consommateur <br> 1:producteur |
| (X & 0xC0) >>6 | (X & 0x3C) >>3 | (X & 0x02) >> 1 | (X & 0x01) |

**Octet 3**
| 23 | 22..21 | 20..19 | 18 | 17 | 16 |
|---|---|---|---|---|---|
| Synchro CPL <br> 0: hors synchro <br> 1: en synchro | Statut CPL, notation binaire <br> 00: New / unlock <br> 01: New / Lock <br> 10: Registered <br> notation décimale fonctionne aussi | Etat sortie com Euridis <br> 0: désactivé <br> 1: Activé sans sécurité <br> 2: non utilisé <br> 3: Activé avec sécurité | non utilisé <br> toujours 0 | Sortie téléinformation <br> 0: mode historique <br> 1: mode standard <br><br> _Amusant car l'étiquette n'existe pas en mode historique_ | Horloge interne <br> 0: horloge correcte <br> 1: horloge dégradée, perte synchro |
| (X & 0x80) >> 7 | (X & 0x60) >> 5 | (X & 0x18) >>3 | (X & 0x04 ) >> 2 | (X & 0x02) >> 1| (X & 0x01) |

**Octet 4**
|31..30 | 29..28 | 27..26 | 25..24 |
|---|---|---|---|
| Pointe mobile <br> 0: Pas de pointe mobile <br> 1: PM1 en cours <br> 2: PM2 en cours <br> 3: PM3 en cours | Péavis pointe mobile <br> 0: Pas de préavis pointe mobile <br> 1: préavis PM1 en cours <br> 2: préavis PM2 en cours <br> 3: préavis PM3 en cours | Couleur lendemain Tempo <br> 0: pas d'annonce  ou hors contrat Tempo <br> 1: Bleu <br> 2: Blanc <br> 3: rouge | Couleur Tempo du jour <br> 0: pas d'annonce  ou hors contrat Tempo <br> 1: Bleu <br> 2: Blanc <br> 3: rouge |
| (X & 0xC0) >>6 | (X & 0x30) >> 4 | (X & 0x0C) >> 2 | (X & 0x03) |
