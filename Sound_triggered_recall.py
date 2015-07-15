
from psychopy import core, data, event, visual, gui, sound
from pykeyboard import PyKeyboard
import OSC, threading, time, csv, os
import random

# ---------------------------------------------
#---- OSC functions
# ---------------------------------------------
k = PyKeyboard()

def left_pressed(addr, tags, data, source):
    if (data[0] == 1.0):
        k.release_key(k.left_key)
    
def right_pressed(addr, tags, data, source):
    if (data[0] == 1.0):
        k.release_key(k.right_key)
# ---------------------------------------------
#---- setup connection with OSC
# ---------------------------------------------
IPAD_IP = '128.237.167.81'


server = OSC.OSCServer(('0.0.0.0', 8000))
client = OSC.OSCClient()
client.connect((IPAD_IP, 9000))

server.addDefaultHandlers()

server.addMsgHandler('/1/left', left_pressed)
server.addMsgHandler('/1/push2', right_pressed)


print "Registered callback functions are: "
for addr in server.getOSCAddressSpace():
    print addr

print "\nStarting OSCServer."
st = threading.Thread(target=server.serve_forever)
st.start()

#----------------------------------------------
#---- data logging
#----------------------------------------------
expName = 'FE_triggered_recall'
expInfo={'participant':'', 'session':'001'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

header = ['FE']
csv_file = open('data/FE retell/FE_list_participant' + expInfo['participant'] + '-' + expInfo['session'] + '.csv', 'w+')
writer = csv.writer(csv_file)
writer.writerow(header)

# ---------------------------------------------
#---- setup the Window
# ---------------------------------------------

window = visual.Window(size = [1920, 1200],
    pos = [0, 0],
    color='white',
    units = u'pix',
    fullscr = True,
    screen = 1,
    allowGUI = False
    )
    


# ---------------------------------------------
# ---- Initialise components for routine: trial
# ---------------------------------------------
directory = os.getcwd()

Image = visual.ImageStim(window, pos=(0, 0))

fes = ["purr.wav", "poke.wav", "tiktok.wav", "ringing_alarm.wav", "shake_nobreak.wav"] 


# ---------------------------------------------
#---- run the trials
# ---------------------------------------------
size = 10.0
index = 0

fe_on = False

sound_path = "fe\\"

def close_server():
    print "\nClosing OSCServer."
    server.close()
    print "Waiting for Server-thread to finish"
    st.join()
    print "Done"
   
while True:
    #refresh the screen
    window.flip()
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]):
        close_server()

        event.clearEvents()
        core.quit()
    
    # check for previous images (the [left] key)
    elif event.getKeys(["left"]):
        if index == 0:
            continue
        if (fe_on == True):
            fe_on = False
            FE.stop() 
        index = index - 1
        
    # check for next images (the [right] key)     
    elif event.getKeys(["right"]):
        if (fe_on == True):
            fe_on = False
            FE.stop()
            
        if (len(fes) == 0):
            close_server()
            
            event.clearEvents()
            #window.close()
            core.quit()
        
        if (len(fes) != 0 and fe_on == False):
            index = random.randint(0, len(fes)-1)
            play_fe = fes[index]
            print(play_fe)
            FE = sound.SoundPyo(sound_path+play_fe)
            FE.setLoops(4)
            FE.play()
            msg = [play_fe]
            writer.writerow(msg)
            fes.remove(play_fe)
            fe_on = True
            
    #clear event
    event.clearEvents()




#end of this routine
#window.close()
core.quit()
 