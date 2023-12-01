<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" /><style>
		body {font-family: Helvetica, sans-serif; font-size:0.8em; min-width:300px;margin:auto;padding:15px;background: #e6f7ff;}
		.couleurjour{width:100%; height:auto; text-align: center; margin-left: auto; margin-right: auto;}
		.bleu,.blanc,.rouge,.indetermine{min-width: 70px; width:auto; max-width:120px;height:auto; margin: auto; border: 1px solid; border-radius: 10px; padding: 3px;font-weight:bold;margin-bottom:2px;}
		.bleu {background: #0000e6; color:#FFF; border-color:#0000e6;}
		.blanc {background: #FFF; color:#000;border-color:#ccc;}
		.rouge {background: #e60000; color:#FFF;border-color:#e60000;}
		.indetermine {background: #ccc; color:#000;border-color:#ccc;}
		.clear{clear: both;}
		.meteos{width:auto;margin: auto;}
		.meteo{width:70px;height:auto;text-align: center;border: 1px solid #ccc;font-size:0.8em;float: left;border-radius: 5px; margin-right:2px; margin-top:1px; padding-bottom:5px;background: #FFF;}
		.meteo br{padding-bottom:2px;}
		.m01d,.m01n,.m02d,.m02n,.m03d,.m03n,.m04d,.m04n,.m09d,.m09n,.m10d,.m10n,.m11d,.m11n,.m13d,.m13n,.m50d,.m50n,.m00{
			width: 50px; height: 50px; margin-left: auto; margin-right: auto; position: relative; background-repeat: no-repeat;
		}
		{{var:__meteocss__}}
</style></head><body>
<div id=\"content\">
<p>Bonjour les Suzois,</p>
<p>Il est {{var:__heure__}}, le soleil de lève à {{var:__sunrise__}} et se couche à {{var:__sunset__}}.<br>Les dernières infos de couleur du linky:</p>
<div class=\"couleurjour\"><div class=\"{{var:__couleurj__:indetermine}}\">aujourd'hui</div><div class=\"{{var:__couleurj1__:indetermine}}\">demain</div></div>
<div class=\"clear\"></div>
<p>Il restera à planifier {{var:__nbrouges__:999}} jours rouges et {{var:__nbblancs__:999}} jours blancs</p>
<p>La météo des 24 prochaines heures</p>
<div class=\"meteos\">
{{var:__meteohtml__}}
</div></div></body></html>