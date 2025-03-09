# import required module
from playsound import playsound

soundlibpath = '/home/pi/bot/src/bot/applicate_bot/applicate_bot/modules/sounds/'
audio1 = 'audio.mp3'
# Boss Janear, pagawa ng mga mp3 files nito po. maiiksing salita lang mga 2 to 3 seconds, 5 max po.
# kahit text to speech nalang po or kung anong balak mo. english o tagalog, kayo bahala
# yung may (OP), optional. di ko pa magagamit yon, pero maigi narin kung meron po.
# lahat ito ay hindi man paulit ulit na asabihin na naka loop. isang beses lang tas may agawin na yung robot
audios = {
    'loading'       :   'Loading.mp3',              # pagka simula ng robot
    'activated'     :   'Activated.mp3',            # pag ready na yung robot
    'cmd_got'       :   '', # pag tapos na ilagay yung utos
    'password'      :   'Password.mp3',             # pag a-enter yung passowrd
    'wrong_pw'      :   'Password_incorrect.mp3',  # pag mali yung passowrd
    'put_item'      :   'Putting_an_item.mp3',      # pag alagay yung gamit
    'heavy'         :   'Heavy.mp3',                # pag mabigat yung nalagay
    'arrived'       :   'Item_arrived.mp3',             # pag naka rating na sa destination maliban sa base/home nya
    'locked'        :   'Storage_lock.mp3',         # pag a-lock yung robot
    'unlocked'      :   'Storage_unlocked.mp3',     # pag a-buksan yung robot
    'remove_item'   :   'Remove_item.mp3',          # pag sasabihan na tagtagin yung gamit
    'leaving'       :   'Nova_is_now_leaving.mp3',  # pag aalis na yung robot

    'error'         :   '', # (OP) pag may mali na di natin alam
    'running'       :   '', # (OP) pag umaandar na yung robot
    'finish'        :   'Task_is_completed.mp3',    # (OP) pag tapos na yung delivery at naka uwi na sya
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