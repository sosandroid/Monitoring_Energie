# Denky

Script Berry pour récupérer les données TIC et les transmettre à EmonCMS. *A personnaliser avec votre configuration*  
**A noter :** l'import du module `string` échoue parfois. Je ne sais pas pourquoi. Dans ces cas là, la seule solution est de commenter les lignes en question. A tester avec [berry console](https://berry-lang.github.io/try-online/)

````berry
import json
import string

var api_url = "http://192.168.1.1/input/post" # persoanlize the URL
var api_key = "YOUR EMONCMS API KEY" # persoanlize the API Key
var node_name = "LINKY" # persoanlize node name
var post_every = 15000 # post evert 15 seconds
var payload = {}

def send_emoncms()
  # Convert JSON object to string 
  var obj_json = json.dump(payload)

  # Create URL to call
  var param="?fulljson="+obj_json + "&node="+node_name + "&apikey="+api_key 
  # Post Data to EMONCMS
  var cl = webclient()
  cl.begin(api_url + param)
  var r =  cl.GET()
  tasmota.set_timer(post_every, send_emoncms)
  #print(api_url + param)
end


# set global payload the field we need
def rule_tic(value, trigger)
  # EAST Index de soutirage total
  # EASF01 index heures creuses
  # EASF02 index heures pleines
  # EAIT Energie active injectée totale
  # SINSTS Puissance app. Instantanée soutirée
  # SINSTI Puissance app. Instantanée injectée

  payload['IDX_SOUT'] = value['EAST'] / 1000.0
  payload['IDX_SOUT_HP'] = value['EASF02'] / 1000.0
  payload['IDX_SOUT_HC'] = value['EASF01'] / 1000.0
  payload['IDX_INJ'] = value['EAIT'] / 1000.0
  payload['PUI_SOUT'] = value['SINSTS']
  payload['PUI_INJ'] = value['SINSTI']
  #Facilite le calcul dans EmonCMS
  payload['PUI_SOUT-INJ'] = value['SINSTS'] - value['SINSTI']

  # Tempo contract - see Enedis-NOI-CPT_54E.pdf
  # Couleur jour et demain
  var regstatus = bytes(value['STGE'])
  payload['TARIF_COULEUR'] = regstatus.get(0,1) & 0x03
  payload['TARIF_COULEUR_DEMAIN'] = (regstatus.get(0,1) & 0x0C) >> 2
  # Période tarification HP / HC
  if string.find(value["LTARF"], 'HP') >= 0
      payload['TARIF_CRENEAU'] = 2
  elif string.find(value['LTARF'], "HC") >= 0
      payload['TARIF_CRENEAU'] = 1
  else
      payload['TARIF_CRENEAU'] = 0 
  end
end

def start()
  # Callback on each frame interception
  tasmota.add_rule("TIC",rule_tic)
  # fire first post in 5s 
  tasmota.set_timer(5000, send_emoncms)
end

# delay start to have time to get full frame
tasmota.set_timer(10000, start)

````


# Pvoutput
A travailler.
Time en Berry => https://tasmota.github.io/docs/Berry/#tasmota-object
