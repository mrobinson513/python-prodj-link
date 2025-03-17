#!/usr/bin/env python3

import curses, logging, socket, json

import requests
from prodj.core.prodj import ProDj
import prodj.network.packets_dump as pdump

# init logging
default_loglevel=logging.INFO
logging.basicConfig(level=default_loglevel)

p = ProDj()
p.set_client_keepalive_callback(lambda n: get_live_track_id())
p.set_client_change_callback(lambda n: get_live_track_id())

def get_live_track_id():
  try:
    decks,data = p.cl.clients,{"track_data": None}
    decks_playing = sum(1 for d in decks if d.play_state == "playing")
    print(decks_playing)
    
    if decks_playing == 1:
      for d in decks:
        print(d.play_state)
        if d.play_state == "playing":
          md = d.metadata
          data["track_data"] = {
            "artist": md["artist"],
            "title": md["title"]
          }
    logging.info(data)
    return json.dumps(data)
  except:
    logging.warn("No valid data yet...")

# update_clients(client_win)

try:
  p.start()
  p.vcdj_enable()
  p.join()
except KeyboardInterrupt:
  logging.info("Shutting down...")
  p.stop()

