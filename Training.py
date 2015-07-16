from psychopy import core, data, event, visual, gui, sound
from pykeyboard import PyKeyboard
import OSC, threading, time, csv, os

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
IPAD_IP = '128.237.164.82'


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

images = [] 
path = directory + "\\trial\\"

for file in os.listdir(path):
    images.append(file)

# ---------------------------------------------
#---- run the trials
# ---------------------------------------------
size = 10.0
index = 0

fe_on = False

image_path = "trial\\"
sound_path = "fe\\"

def close_server():
    print "\nClosing OSCServer."
    server.close()
    print "Waiting for Server-thread to finish"
    st.join()
    print "Done"
   
while True:
    Image.setImage(image_path+images[index])
    Image.draw(window)
    if ((index == 0) and (fe_on == False)):
        FE = sound.SoundPyo(sound_path+"swipe_trial.wav")
        FE.setLoops(10)
        FE.play()
        fe_on = True
        
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
            
        #print("Key press to index:" + str(index))
        if index == (len(images)-1):
            print('index' + str(index))
            print('len' + str(len(images)))
            
            close_server()
            
            event.clearEvents()
            #window.close()
            core.quit()
        index = index +1
    #clear event
    event.clearEvents()




#end of this routine
#window.close()
core.quit()
 