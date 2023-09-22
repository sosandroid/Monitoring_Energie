import json

var api_url = "http://192.168.1.1/input/post"
var api_key = "YOUR EMONCMS API KEY"
var node_name = "LINKY"
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
  # EASF01 index heures pleines
  # EASF02 index heures creuses
  # EAIT	Energie active injectée totale
  # SINSTS Puissance app. Instantanée soutirée
  # SINSTI	Puissance app. Instantanée injectée
  # Got Heures Creuses contract so I will calculate total consumption

  payload['IDX_SOUT'] = value['EAST'] / 1000.0
  payload['IDX_SOUT_HC'] = value['EASF01'] / 1000.0
  payload['IDX_SOUT_HP'] = value['EASF02'] / 1000.0
  payload['IDX_INJ'] = value['EAIT'] / 1000.0
  payload['PUI_SOUT'] = value['SINSTS']
  payload['PUI_INJ'] = value['SINSTI']
  #Facilite le calcul dans EmonCMS
  payload['PUI_SOUT-INJ'] = value['SINSTS'] - value['SINSTI']

end

def start()
  # Callback on each frame interception
  tasmota.add_rule("TIC",rule_tic)
  # fire first post in 5s 
  tasmota.set_timer(5000, send_emoncms)
end

# delay start to have time to get full frame
tasmota.set_timer(10000, start)