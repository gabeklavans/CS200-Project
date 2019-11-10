import re
import csv
import operator
from pathlib import Path

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
smol = re.sub('.*(Program).*\n', '', smol)
# Normalize to one track
smol = re.sub('\n\d', '\n1', smol)
# Remove header
smol = re.sub('.*(Header).*\n', '', smol)

big_csv = csv.reader(open('alb.csv',encoding='cp1252'),delimiter=',')

# TODO: Make it sort by number value instead of string

sortedlist = sorted(big_csv, key=operator.itemgetter(1))
print(sortedlist)
# now write the sorte result into new CSV file
# with open("NewFile.csv", "wb") as f:
#     fileWriter = csv.writer(f, delimiter=',')
#     for row in sortedlist:
#         fileWriter.writerow(row)
list = ""
for item in sortedlist:
    line = ""
    for c in item:
        line += c
        line += ","
    list += line
    list += "\n"

print(list)
