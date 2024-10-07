# import required module
from playsound import playsound

soundlibpath = '../sound/'
def play(filename):
    playsound(soundlibpath + filename)

# backup for linux specifically (native player)
# import required module
import os

# play sound
file = "note.mp3"
print('playing sound using native player')
os.system("mpg123 " + file)