# import required module
from playsound import playsound

soundlibpath = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/sounds/'
audio1 = 'audio.mp3'
audios = {
    'loading': 'loading.mp3', #super optional
    'activated' : 'activated.mp3',
    'cmd_got': 'cmd_got.mp3',
    'running' : 'running.mp3',
    'password': 'password.mp3',
    'put_item' : 'put_item.mp3',
    'heavy': 'heavy.mp3',
    'finish' : 'finish.mp3',
    # 'nothing' : 'nothing.mp3' # not in list, play nothing
    # 'error': '',
    # 'arrived': '',
    # 'locked': '',
    # 'unlocked': '',
    # 'open': '',
    # 'clode': '',
    # 'remove_item': '',
    # 'leaving': ''
    
}
def playfor(soundlibpath, situation):
    if audios.get(situation) is not None:
        playsound(soundlibpath + audios[situation])
    # else:
    #     playsound(soundlibpath + audios["nosounderror"])
    pass

        
# # backup for linux specifically (native player)
# # import required module
# import os

# # play sound
# file = "note.mp3"
# print('playing sound using native player')
# os.system("mpg123 " + file)