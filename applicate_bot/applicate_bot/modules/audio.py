# import required module
from playsound import playsound

soundlibpath = '../sound/'
audio1 = 'audio.mp3'
audios = {
    'situation1': 'audio.mp3',
    'nosounderror' : 'nserr.mp3'
}
def playfor(situation):
    if audios.get(situation) is not None:
        playsound(soundlibpath + audios[situation])
    else:
        playsound(soundlibpath + audios["nosounderror"])
    pass

        
# # backup for linux specifically (native player)
# # import required module
# import os

# # play sound
# file = "note.mp3"
# print('playing sound using native player')
# os.system("mpg123 " + file)