# -----------------------------------------------------------------------
#
# (c) Copyright 2015 Siyan Zhao @ Disney Research Pittsburgh
#
# -----------------------------------------------------------------------

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This experiment was created using PsychoPy2 Experiment Builder
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce (2007) Journal of Neuroscience Methods 162:8-1
  Peirce (2009) Frontiers in Neuroinformatics, 2: 10"""

from iViewXAPI import  *            			#iViewX library
from numpy import *                   			#many different maths functions
from numpy.random import *       				#maths randomisation functions
import os                                   	#handy system and path functions
from psychopy import core, data, event, visual, gui, sound
import psychopy.logging                   		#import like this so it doesn't interfere with numpy.log
import pygame
from pykeyboard import PyKeyboard
import OSC, threading, time, csv

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
# ---------------------------------------------
#---- store info about the experiment
# ---------------------------------------------

expName = 'GazeContingent'
expInfo={'participant':'', 'session':'001'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName


# ---------------------------------------------
#---- setup files for saving
# ---------------------------------------------

if not os.path.isdir('data'):
    os.makedirs('data')
    #if this fails (e.g. permissions) we will get error

psychopy.logging.console.setLevel(psychopy.logging.warning)
#this outputs to the screen, not a file
path_data = os.getcwd() + "\\data\\"
filename='%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=psychopy.logging.LogFile(path_data+filename+'.log', level=psychopy.logging.EXP)
description = expInfo['session']
participant = expInfo['participant']
print "filename: " + filename
print "description: " + description


# ---------------------------------------------
#---- connect to iView
# ---------------------------------------------

res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("iViewXSDK_Python_GazeContingent_Demo.txt"))
res = iViewXAPI.iV_Connect(c_char_p('127.0.0.1'), c_int(4444), c_char_p('127.0.0.1'), c_int(5555))
if res != 1:
    HandleError(res)
    exit(0)
    
res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
print "iV_GetSystemInfo: " + str(res)
print "Samplerate: " + str(systemData.samplerate)
print "iViewX Verion: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
print "iViewX API Verion: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)


# ---------------------------------------------
#---- configure and start calibration
# ---------------------------------------------
geom = CREDGeometry(1, 0, 20, 36, "D", 520, 325)
res = iViewXAPI.iV_SetREDGeometry(byref(geom))
print "redGeometry " + str(geom.redGeometry)

#displayDevice = 1
#calibrationData = CCalibration(5, 1, displayDevice, 0, 1, 20, 239, 1, 10, b"")
#
#res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
#print "iV_SetupCalibration " + str(res)
#res = iViewXAPI.iV_Calibrate()
#print "iV_Calibrate " + str(res)
#outputfile = path_data + filename
#iViewXAPI.iV_SaveCalibration(outputfile)
#
#res = iViewXAPI.iV_Validate()
#print "iV_Validate " + str(res)
#
#res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 1)
#print "iV_GetAccuracy " + str(res)
#print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
#print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY)
#
#while (accuracyData.deviationLX > 1) or (accuracyData.deviationLY > 1):
#    res = iViewXAPI.iV_Calibrate()
#    print "iV_Calibrate " + str(res)
#    outputfile = path_data + filename
#    
#    res = iViewXAPI.iV_Validate()
#    print "iV_Validate " + str(res)
#    
#    res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), 1)
#    print "iV_GetAccuracy " + str(res)
#    print "deviationXLeft " + str(accuracyData.deviationLX) + " deviationYLeft " + str(accuracyData.deviationLY)
#    print "deviationXRight " + str(accuracyData.deviationRX) + " deviationYRight " + str(accuracyData.deviationRY)

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
path = directory + "\\inks\\"

for file in os.listdir(path):
    images.append(file)

trialClock=core.Clock()
Shape01 = visual.Circle(win=window, edges=64, radius=8, opacity=1)


# ---------------------------------------------
#---- run the # ---------------------------------------------
size = 10.0
index = 0

image_path = "inks\\"
sound_path = "fe\\"

#detect if data log has begun of not
data_log = False

fe_on = False
trial_clock = core.Clock()
start_time = 0
header = ['image', 'FE?', 'start time', 'end time', 'duration']
csv_file = open('data/participant' + expInfo['participant'] + '-' + expInfo['session'] + '.csv', 'w+')
writer = csv.writer(csv_file)
writer.writerow(header)

iViewXAPI.iV_StartRecording()

def smi_save():
    iViewXAPI.iV_StopRecording()
    outputfile = path_data + filename
    print(outputfile)
    print(participant)
    data_save = iViewXAPI.iV_SaveData(str(outputfile), str(description), str(participant), 1)
    if data_save != 1:
        err = errorstring(data_save)
        raise Exception("error: failed to save data; %s" % err)
    print 'iV_SaveData ' + str(data_save)
    print "data saved to: " + outputfile
    
    iViewXAPI.iV_Disconnect()
        
def close_server():
    print "\nClosing OSCServer."
    server.close()
    print "Waiting for Server-thread to finish"
    st.join()
    print "Done"
    
def write_txt(img, on_off, start, end, dur):
    msg = [img, on_off, start, end, dur]
    writer.writerow(msg)
    
while True:

	# update gaze event 
    res = iViewXAPI.iV_GetEvent(byref(eventData))
    
	# update gaze data sample
    res = iViewXAPI.iV_GetSample(byref(sampleData))
    if res == 1:
        Image.setImage(image_path+images[index])
        Image.draw(window)
        
        # Log the first image
        if ((index == 0) and (not data_log)):
            iViewXAPI.iV_SendImageMessage(c_char_p(images[index]))
            data_log = True
        
        # Play haptic effects as sound when certain frames come up
        if ((index == 0) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"ringing_alarm.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 2) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"creature.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
        
        if ((index == 7) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"push.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 9) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"purr.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 15) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"shake_nobreak.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 17) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"poke.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 20) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"poke.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 21) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"tiktok.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 25) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"rain.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 27) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"heartbeat.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
        if ((index == 30) and (fe_on == False)):
            FE = sound.SoundPyo(sound_path+"tap_edited.wav")
            FE.setLoops(10)
            FE.play()
            fe_on = True
            
#        Shape01.setFillColor([0, 0, 0])
#        sampleData.leftEye.gazeX = sampleData.leftEye.gazeX - 640
#        sampleData.leftEye.gazeY = -1 * (sampleData.leftEye.gazeY - 512)
#        Shape01.setPos([sampleData.leftEye.gazeX - size, sampleData.leftEye.gazeY - size])
#        Shape01.draw()

    #refresh the screen
    window.flip()
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]):
        smi_save()
        close_server()

        event.clearEvents()
        core.quit()
    
    # check for previous images (the [left] key)
    elif event.getKeys(["left"]):
        if index == 0:
            continue
        print("left")
        end_time = trial_clock.getTime()
        dur = end_time - start_time
        write_txt(images[index], fe_on, start_time, end_time, dur)
        start_time = end_time
        index = index - 1
        iViewXAPI.iV_SendImageMessage(c_char_p(images[index]))
        
        if (fe_on == True):
            FE.stop() 
            fe_on = False
        
    # check for next images (the [right] key)     
    elif event.getKeys(["right"]):
        end_time = trial_clock.getTime()
        dur = end_time - start_time
        write_txt(images[index], fe_on, start_time, end_time, dur)
        start_time = end_time
        if (fe_on == True):
            FE.stop()
            fe_on = False
        #print("Key press to index:" + str(index))
        if index == (len(images)-1):
            print('index' + str(index))
            print('len' + str(len(images)))
            
            smi_save()
            close_server()
            
            event.clearEvents()
            #window.close()
            core.quit()
        index = index +1
        iViewXAPI.iV_SendImageMessage(c_char_p(images[index]))

    #clear event
    event.clearEvents()




#end of this routine
#window.close()
core.quit()
