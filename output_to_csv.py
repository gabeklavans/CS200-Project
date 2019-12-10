from pathlib import Path
import sys

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def char_to_midi(char: str) -> int:
    char_val = ord(char)

    if char_val < 33:
        # print(chr(char_val))
        return -1
    elif char_val <= 47:
        return (char_val - 9)
    elif char_val <= 126:
        return (char_val - 19)
    else:
        return -2

input_txt = Path(sys.argv[1]).read_text()  # encoding='cp1252')

# split up string into space-separated values
data = input_txt.split(' ')

timings = [['0', '0', 'Header', '1', '1', '480'], ['1', '0', 'Start_track']]

current_time = 0
# loop through all characters and do processing
for value in data:
    if is_number(value):
        current_time += int(value)
    else:
        i = 0
        while i < len(value):
            # remove this statement for debugging
            if char_to_midi(value[i]) < 0:
                i += 1  # skip it
            elif value[i] == '.':
                timings.append(['1', str(current_time), 'Note_on_c',
                                '0', str(char_to_midi(value[i+1])), '0'])
                i += 2
            else:
                timings.append(['1', str(current_time), 'Note_on_c',
                                '0', str(char_to_midi(value[i])), '100'])
                i += 1

timings.append(['1', str(current_time), 'End_track'])
timings.append(['0', '0', 'End_of_file'])

output = '\n'.join([", ".join(line) for line in timings])

print(output)
