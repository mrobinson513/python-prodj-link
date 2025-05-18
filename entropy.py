import json,time,os
import logging

from obswebsocket import obsws, requests as actions

default_loglevel=logging.DEBUG
logging.basicConfig(level=default_loglevel)

OBS_WEBSOCKET_HOST=os.getenv("OBS_WEBSOCKET_HOST", "localhost")
OBS_WEBSOCKET_PORT=os.getenv("OBS_WEBSOCKET_PORT", "4455")
OBS_GLITCH_MAX_TIME=os.getenv("OBS_GLITCH_MAX_TIME", 7200000)

obs = obsws(OBS_WEBSOCKET_HOST, 4455, "")
logging.info("Connecting to OBS WebSocket...")
obs.connect()
logging.info("Verifying...")
obs_version = obs.call(actions.GetVersion()).getObsVersion()
logging.info(f"OBS Version: {obs_version}")

while True:
  rec = obs.call(actions.GetRecordStatus())
  current_duration = rec.datain['outputDuration']
  expected_duration = 7200000 # 7.2M milliseconds
  pct_duration = current_duration / expected_duration * 100
  obs.call(actions.SetSourceFilterSettings(
    sourceName="Header",
    filterName="header_glitch",
    filterSettings={
      'digital_glitch_amount': pct_duration
      }
    )
  )
  time.sleep(60)
