import re
import csv
import operator
from pathlib import Path
import numpy as np
import sys

# string = "1, 0, Time_signature, 3, 2, 24, 8\n\
# 1, 0, Key_signature, -1, \"major\"\n\
# 1, 0, Tempo, 642192\n\
# 1, 480, Tempo, 617920\n\
# 1, 1440, Tempo, 563380\n\
# 1, 1920, Tempo, 533333\n\
# 1, 2160, Tempo, 538117\n\
# 1, 2200, Tempo, 524017\n"

string = Path(
    '/Users/cassandra/GitHub/CS200-Project/alb.txt').read_text(encoding='cp1252')

# Remove track/file info
smol = re.sub('.*(Start|End).*\n', '', string)
# Remove metadata stuff
smol = re.sub('.*(_t|SMPTE|Time|Key).*\n', '', smol)
# Remove tempo markings
smol = re.sub('.*(Tempo).*\n', '', smol)
# Don't know what this does but we don't need it soooo
smol = re.sub('.*(Program|Control).*\n', '', smol)
# Normalize to one track
smol = re.sub('\n\d', '\n1', smol)
# Remove header
smol = re.sub('.*(Header).*\n', '', smol)

# Convert to an array values from the CSV
data = []

for line in smol.splitlines():
    line = [v.strip() for v in line.split(',')]
    data.append(line)

# put the timings in a data stucture in the form [time, note, velocity]
# velocities are used for either on or off cuz we want those spicy note lengths
timings = [[int(row[1]),int(row[4]),int(row[5])] for row in data]

# sort the timings by time, so all chords are fully kept together
timings = np.array(timings)
timings = np.sort(timings.view('i8,i8,i8'), order=['f0'], axis=0).view(np.int)

# the final output string
output = ""

# initialize last time to the first event time
last_time = timings[0][0]

for line in timings:
    time = line[0]
    note = line[1]
    velocity = line[2]

    if (time - last_time) > 0:
        diff = time - last_time
        output += f' {diff} '
    # TODO: Map the MIDI input number to the ASCII character i want
    # getMap(note)
    output += "A"
    if velocity == 0:
        output += "."
    last_time = time
    

np.set_printoptions(threshold=sys.maxsize)
print(output)
