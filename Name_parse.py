FILENAME = "top200.csv"
TARGETFILENAME = FILENAME[0:-4] + "_parsed.csv"
FFfile = open(FILENAME)
lines = FFfile.readlines()
FFfile.close()
newlines = []
for l in lines:
    splitline = l.split(',')
    line1 = splitline[0].strip('"')
    player_split = line1.split()
    rank = player_split[0].rstrip('.')
    first_name = player_split[1]
    last_name = player_split[2].rstrip(',')
    position = splitline[1].rstrip('"').strip()
    newline = rank + "," + last_name + "," + first_name + "," + position + \
              "," + splitline[2] + "," + splitline[3]
    newlines.append(newline)

newlines = ''.join(newlines)
print newlines
targetfile = open(TARGETFILENAME, 'w')
targetfile.write(newlines)
targetfile.close()
print 'DONE!'


    
    
