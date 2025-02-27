import json,time
import logging

from flask import Flask
from prodj.core.prodj import ProDj

default_loglevel=logging.DEBUG
logging.basicConfig(level=default_loglevel)

#p.set_client_keepalive_callback(lambda n: get_decks())
#p.set_client_change_callback(lambda n: get_decks())
#p.join()

app = Flask("__main__")
print("did flask start?")

p = ProDj()
p.start()
p.vcdj_enable()
p.vcdj_set_player_number(5)
#p.join()

@app.route("/")
def index():
  decks,data = p.cl.clients,{"live": None}
  decks_playing = sum(1 for d in decks if d.play_state == "playing")
  print(decks_playing)
  
  if decks_playing == 1:
    for d in decks:
      print(d.play_state)
      if d.play_state == "playing":
        md = d.metadata
        data["live"] = {
          "artist": md["artist"],
          "title": md["title"]
        }
  else:
    data["live"] = "no decks playing or none found"
  print(data)
  return json.dumps(data)

#p.stop()