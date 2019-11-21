from pathlib import Path

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def char_to_midi(char: str) -> int:
    char_val = ord(char)

    if char_val < 33:
        #print(chr(char_val))
        return -1
    elif char_val <= 47:
        return (char_val - 9)
    elif char_val <= 126:
        return (char_val - 19)
    else:
        return -2

input_txt = Path(
    '/Users/cassandra/GitHub/CS200-Project/output.txt').read_text()#encoding='cp1252')

#print(input_txt)

# split up string into space-separated values
data = input_txt.split(' ')

timings = []

current_time = 0
# loop through all characters and do processing
for value in data:
    if is_number(value):
        current_time += int(value)
    for i in range(len(value)):
        # remove this statement for debugging
        if char_to_midi(value[i]) < 0:
            pass # skip it
        elif value[i] == '.':
            timings.append([current_time, char_to_midi(value[i+1]), 0])
        else:
            timings.append([current_time, char_to_midi(value[i]), 100])

print(timings)