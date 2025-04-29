#!/usr/bin/env python3

from threading import Thread
import time
import math
import mido
import logging
import re

class MidiClock:
    def __init__(self, bpm=120.0):
        self.bpm = bpm
        self.running = False
        self.tick_interval = 60.0 / (self.bpm * 24)

    def open(self,midi_port_name=None):
        if midi_port_name:
            self.outport = mido.open_output(midi_port_name)
        else:
            self.outport = mido.open_output()

    def iter_midi_clients():
        return mido.get_output_names()

    def start(self):
        if not self.running:
            self.running = True
            self.outport.send(mido.Message('start'))

    def stop(self):
        if self.running:
            self.running = False
            self.outport.send(mido.Message('stop'))

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.tick_interval = 60.0 / (self.bpm * 24)

    def send_tick(self):
        if self.running:
            self.outport.send(mido.Message('clock'))

    def run(self):
        try:
            while True:
                if self.running:
                    self.send_tick()
                    time.sleep(self.tick_interval)
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            self.stop()
    


if __name__ == "__main__":
    import sys

    bpm = 120.0
    if len(sys.argv) > 1:
        bpm = float(sys.argv[1])

    clock = MidiClock(bpm)
    clock.start()
    clock.run()
