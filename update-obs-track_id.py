#!/usr/bin/env python

import json,time,os
import logging

from obswebsocket import obsws, requests as actions
from flask import Flask, render_template, redirect, session, request

default_loglevel=logging.DEBUG
logging.basicConfig(level=default_loglevel)

OBS_WEBSOCKET_HOST=os.getenv("OBS_WEBSOCKET_HOST", "localhost")
OBS_WEBSOCKET_PORT=os.getenv("OBS_WEBSOCKET_PORT", "4455")

obs = obsws(OBS_WEBSOCKET_HOST, 4455, "")
logging.info("Connecting to OBS WebSocket...")
obs.connect()
logging.info("Verifying...")
obs_version = obs.call(actions.GetVersion()).getObsVersion()
logging.info(f"OBS Version: {obs_version}")

app = Flask(__name__) # all this is going to do is listen for a POST with a payload, validate it, and push up to the
                      # text box that displays the track ID

@app.route('/')
def index():
  # later we can make this a tiny admin page for identifying the source we're going to edit
  return "<h2>You're not supposed to be here...</h2>"

@app.route('/update', methods=['POST'])
def update(input_name="track_id"):
  if request.method == 'POST':
    try:
      track_data = request.get_json(force=True)['track_data']
      try:
        artist = track_data['artist']
        title = track_data['title']
        track_string = f"{artist}\n\n{title}"
        obs.call(actions.SetInputSettings(
          inputName=input_name,
          inputSettings={
            "text": track_string
          }
        ))
        return "Track data received"
      except KeyError:
        logging.warn("Payload did not contain expected keys, not going to update")
    except:
      error_message = """Proper track data not found. Should be a JSON object containing: 
        {'track_data': {
          'artist': 'artist_name',
          'title': 'track_title'}
        }"""
      logging.error(f"payload received: {request.get_json(force=True)}")
      return error_message

if __name__ == "__main__":
  app.run(host="0.0.0.0",port=8080)