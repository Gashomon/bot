# import required module
from playsound import playsound

soundlibpath = '../sound/'
audio1 = 'audio.mp3'

def playfor(situation):
    if situation == 'running':
        playsound(soundlibpath + audio1)
    elif situation == 'arrived':
        playsound(soundlibpath + audio1)
    elif situation == 'departing':
        playsound(soundlibpath + audio1)
    elif situation == 'password':
        playsound(soundlibpath + audio1)

        
# # backup for linux specifically (native player)
# # import required module
# import os

# # play sound
# file = "note.mp3"
# print('playing sound using native player')
# os.system("mpg123 " + file)