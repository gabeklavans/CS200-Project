# This will attempt to convert all .csv files in current directroy 
# into input files for the model
import re
import csv
import operator
from pathlib import Path
import numpy as np
import sys, glob
np.set_printoptions(threshold=sys.maxsize)

# Converts a midi note number to an ascii character
# Can only handle C1 - B7
def midi_to_char(midi: int) -> str:
    if midi < 24:
        return "NOTE_TOO_LOW_AHHHH"
    elif midi <= 38:
        return chr(midi + 9)
    elif midi <= 107:
        return chr(midi + 19)
    else:
        return "NOTE_TOO_HIGH_AHHHH"

def getInputString(fileName):

    string = Path(fileName).read_text(encoding='cp1252')

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

    #print(smol)

    # Convert to an array values from the CSV
    data = []

    for line in smol.splitlines():
        line = [v.strip() for v in line.split(',')]
        data.append(line)

    # put the timings in a data stucture in the form [time, note, velocity]
    # velocities are used for either on or off cuz we want those spicy note lengths
    timings = [[int(row[1]), int(row[4]), int(row[5])] for row in data]

    # sort the timings by time, so all chords are fully kept together
    timings = np.array(timings)
    timings = np.sort(timings.view('i8,i8,i8'), order=['f0'], axis=0).view(np.int)

    # the final output string
    output = ""

    # initialize last time to the first event time
    last_time = timings[0][0]

    for line in timings:
        time = line[0]
        note_num = line[1]
        velocity = line[2]

        if (time - last_time) > 0:
            diff = time - last_time
            output += f' {diff} '
        if velocity == 0:
            output += "~"
        output += midi_to_char(note_num)
        last_time = time

    return output

for arg in glob.glob('*.csv'):
    #print('Arg:',arg,'Output:')
    print(getInputString(arg))