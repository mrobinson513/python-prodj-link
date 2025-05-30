#!/usr/bin/env python3

import curses, logging, socket, json, os

import requests
from prodj.core.prodj import ProDj
import prodj.network.packets_dump as pdump

# init logging
default_loglevel=logging.INFO
logging.basicConfig(level=default_loglevel)

# init vars
ENDPOINT_HOST=os.getenv("ENDPOINT_URL", "localhost")
ENDPOINT_PORT=os.getenv("ENDPOINT_PORT", "8080")
MIDI_DEVICE_NAME=os.getenv("MIDI_DEVICE_NAME", "Elektron Digitakt")

which_os = os.uname().sysname

# this only works on linux/RPi
if which_os == "Linux":
  from prodj.midi.midiclock_alsaseq import MidiClock

  c = MidiClock()
  c.open(MIDI_DEVICE_NAME,0)

  bpm = 128 # default bpm until reported from player
  beat = 0

  c.setBpm(bpm)

p = ProDj()
p.set_client_keepalive_callback(lambda n: get_live_track_id())
p.set_client_change_callback(lambda n: get_live_track_id())

def get_live_track_id():
  global bpm, beat, p, c
  try:
    decks,data = p.cl.clients,{"track_data": None}
    decks_playing = sum(1 for d in decks if d.play_state == "playing")
    
    if decks_playing > 0:
      if decks_playing == 1:
        for d in decks:
          client=p.cl.getClient(d.player_number)
          if d.play_state == "playing":
            md = d.metadata
            data["track_data"] = {
              "artist": str(md["artist"]),
              "title": str(md["title"])
            }
            newbpm = client.bpm*client.actual_pitch
            if which_os == "Linux":
              c.setBpm(newbpm)
              logging.info(f"track BPM: {newbpm}")
      logging.info(data)
    else:
      data["track_data"] = {
        "artist": "",
        "title": "No track presently playing"
      }
    try:
      resp = requests.post(url=f"http://{ENDPOINT_HOST}:{ENDPOINT_PORT}/update", data=json.dumps(data))
      return json.dumps(data)
    except ConnectionError:
      logging.warn("The endpoint is unreachable but don't let that stop you")
  except:
    logging.error("Something is wrong, check other log messages")

# update_clients(client_win)

try:
  p.start()
  p.vcdj_enable()
  p.join()
except KeyboardInterrupt:
  logging.info("Shutting down...")
  p.stop()
