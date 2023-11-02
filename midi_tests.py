# import midi to csv

import csv
import mido
from mido import MidiFile
mid = MidiFile('D:\\MusicProduction\\\mixes\\Cloven Hooves\\Audio\\cloven_hooves_drums.mid')
mid = MidiFile('D:\\MusicProduction\\mixes\\NailtheMix_November2022_AAL_RedMiso_48k32b\\00 Synths Midi.mid')
bpm = mid.ticks_per_beat

midi_data = []

for i, track in enumerate(mid.tracks):
 for msg in track:
     if msg.type == 'meta':
         midi_data.append([i, msg.time, msg.type])
     elif msg.type in ['note_on', 'note_off']:
         midi_data.append([i, msg.time, msg.type, msg.note, msg.velocity])

with open('output.csv', 'w', newline='') as file:
 writer = csv.writer(file)
 writer.writerow(["Track", "Time", "Type", "Note", "Velocity"])
 writer.writerows(midi_data)
