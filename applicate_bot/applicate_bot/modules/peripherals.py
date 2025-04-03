# import required module
from playsound import playsound

import pyautogui

soundlibpath = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/sounds/'
audio1 = 'audio.mp3'
# Boss Janear, pagawa ng mga mp3 files nito po. maiiksing salita lang mga 2 to 3 seconds, 5 max po.
# kahit text to speech nalang po or kung anong balak mo. english o tagalog, kayo bahala
# yung may (OP), optional. di ko pa magagamit yon, pero maigi narin kung meron po.
# lahat ito ay hindi man paulit ulit na asabihin na naka loop. isang beses lang tas may agawin na yung robot
audios = {
    'loading'       :   'Loading.mp3',              # pagka simula ng robot
    'activated'     :   'Activated.mp3',            # pag ready na yung robot
    'cmd_got'       :   'Cmd.mp3', # pag tapos na ilagay yung utos
    'enter_pass'    :   'Password_enter.mp3',             # pag a-enter yung passowrd
    'wrong_pw'      :   'Password_incorrect.mp3',  # pag mali yung passowrd
    'put_item'      :   'Putting.mp3',      # pag alagay yung gamit
    'heavy'         :   'Heavy.mp3',                # pag mabigat yung nalagay
    'arrived'       :   'Arrived.mp3',             # pag naka rating na sa destination maliban sa base/home nya
    'locked'        :   'Lock.mp3',         # pag a-lock yung robot
    'unlocked'      :   'Unlocked.mp3',     # pag a-buksan yung robot
    'remove_item'   :   'Removing.mp3',          # pag sasabihan na tagtagin yung gamit
    'leaving'       :   'Leaving.mp3',  # pag aalis na yung robot
    'show_pass'     :   'Password_show.mp3',
    'notify'        :   'Notify.mp3',

    'hello1'        :   'hi1.mp3',
    'hello2'        :   'hi2.mp3',
    'hello3'        :   'hi3.mp3',

    'error'         :   '', # (OP) pag may mali na di natin alam
    'running'       :   '', # (OP) pag umaandar na yung robot
    'finish'        :   'Complete.mp3',    # (OP) pag tapos na yung delivery at naka uwi na sya
    'nothing'       :   '', # (OP) not in list, play nothing
    'open'          :   '', # (OP) pag bukas yung robot
    'close'         :   '', # (OP) pag sarado yung robot
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

def clickAt(x_coor,y_coor):
    # print(f"clicked at: {x_coor}, {y_coor}")
    pyautogui.click(x=x_coor,y=y_coor)
    pass