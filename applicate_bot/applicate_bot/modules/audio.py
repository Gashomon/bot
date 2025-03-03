# import required module
from playsound import playsound

soundlibpath = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/sounds/'
audio1 = 'audio.mp3'
# Boss Janear, pagawa ng mga mp3 files nito po. maiiksing salita lang mga 2 to 3 seconds, 5 max po.
# kahit text to speech nalang po or kung anong balak mo. english o tagalog, kayo bahala
# yung may (OP), optional. di ko pa magagamit yon, pero maigi narin kung meron po.
# lahat ito ay hindi man paulit ulit na asabihin na naka loop. isang beses lang tas may agawin na yung robot
audios = {
    'loading': '', # pagka simula ng robot
    'activated' : '', # pag ready na yung robot
    'cmd_got': '', # pag tapos na ilagay yung utos
    'password': '', # pag a-enter yung passowrd
    'wrong_pw': '', # pag mali yung passowrd
    'put_item' : '', # pag alagay yung gamit
    'heavy': '', # pag mabigat yung nalagay
    'arrived': '', # pag naka rating na sa destination maliban sa base/home nya
    'locked': '', # pag a-lock yung robot
    'unlocked': '', # pag a-buksan yung robot
    'remove_item': '', # pag sasabihan na tagtagin yung gamit
    'leaving': '' # pag aalis na yung robot

    'error': '', # (OP) pag may mali na di natin alam
    'running' : '', # (OP) pag umaandar na yung robot
    'finish' : '', # (OP) pag tapos na yung delivery at naka uwi na sya
    'nothing' : '' # (OP) not in list, play nothing
    'open': '', # (OP) pag bukas yung robot
    'close': '', # (OP) pag sarado yung robot
}

def playfor(soundlibpath, situation):
    if audios.get(situation) is not None:
        try:
            playsound(soundlibpath + audios[situation])
        except:
            print("cant play sound for " + situation)
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