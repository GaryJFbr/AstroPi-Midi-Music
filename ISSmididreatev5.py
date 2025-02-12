# playing sound from ISS data
# csv file must have roll,pitch,yaw (as a dictionary) data in column 1,
# will work with magnetometer data in column 1
# place csv file in the current working directory
import csv
from midiutil import MIDIFile
import re

# create empty lists for data
# input lists created for the ISS data
RollData =[]
PitchData = []
YawData =[]
# output lists for midi file creation
TimeData =[]
NoteData =[]
SoundData =[]

# Create a file of midi notes and set the beat
# This is the Middle octaves 2,3,4 no sharps
NoteNames = [48,50,52,53,55,57,59,
             60,62,64,65,67,69,71,
             72,74,76,77,79,81,83]
BeatsPerMin = 240 # why? just sounds best

# define a function to map values 
# (or array of values) from one range to another
def map_value(value, MinList, MaxList, MinOutputList, MaxOutputList):
    result = MinOutputList + ((value - MinList)/(MaxList - MinList)*(MaxOutputList - MinOutputList))
    return result

# open the csv file and convert to lists pitch, roll and yaw
ISSfile = open("SampleData2.csv", newline='')
ISSReader = csv.reader(ISSfile)
ISSdata = list(ISSReader) # creates a list of strings 

# read the values into lists
for i in range(0, len(ISSdata)):
    nextitem = ISSdata[i][0]
    RPYvalues=re.findall("\d+\.\d+",nextitem)
# read the data into the list and convert to a float
    RollData.append(float(RPYvalues[0]))
    PitchData.append(float(RPYvalues[1]))
    YawData.append(float(RPYvalues[2]))

# Determine max, min values in each list and how many notes to play
MaxRoll= max(RollData)
MinRoll= min(RollData)

MaxPitch= max(PitchData)
MinPitch= min(PitchData)

MaxYaw= max(YawData)
MinYaw= min(YawData)

NotesToPlay= len(RollData) # 1 list item equals 1 note, could be any of the three Data lists

# Set the constants
# length note to be played in secs
MinTime = 1 # Minimum time a note will be played
MaxTime = 2 # Maximum time a note will be played
# Used to select notes, 0 is note 1 in NoteNames, 20 is note 21
MaxNote = 20
MinNote = 0
# Standard MIDO sound span
MaxSound = 127
MinSound = 20   # 0 = silent


# map ISS data to Midi data Roll to note, Yaw to sound and pitch to time
for i in range (0, NotesToPlay):
    # map roll value to note range and convert to an integer
    NoteSelect=int(map_value(RollData[i], MinRoll, MaxRoll, MinNote, MaxNote))
    # pick the note corresponding to the integer value
    NoteData.append(NoteNames[NoteSelect])
    # map the yaw and time values to the coresponding range
    SoundData.append(int(map_value(YawData[i], MinYaw, MaxYaw, MinSound, MaxSound)))
    TimeData.append(int(map_value(PitchData[i], MinPitch, MaxPitch, MinTime, MaxTime)))

#create midi file object, add tempo
ISSmidifile = MIDIFile(1) #one track 
ISSmidifile.addTempo(track=0, time=0, tempo=BeatsPerMin) 
#add midi notes
for i in range(len(TimeData)):
    ISSmidifile.addNote(track=0, channel=0, time= TimeData[i] + i, pitch= NoteData[i], volume= SoundData[i], duration=2)
#create and save the midi file itself
with open('ISSsoundstrack1.mid', "wb") as f:
    ISSmidifile.writeFile(f)
    # confirm completion
    print("Done")
