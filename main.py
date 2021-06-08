import sys
import os
import threading
import logging
import subprocess
import socketio
from dialog import Dialog
from audioManager import AudioRecorder
from faceManager import FaceRecognition
logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)

#Connect to Socket
sio = socketio.Client()

#listen en pitch event
@sio.on('pitch', namespace='/speech')
def on_pitch(data):
    tt=data['content']
    dialog.SpeakText(tt)

def main():
    
    #Connexion au serveur
    sio.connect('http://192.168.252.216:9400', namespaces=['/speech'])
    print('my sid is', sio.sid)
    #sio.on("pitch",message,namespace=['/speech'])
    sio.wait()

if __name__ == "__main__":
    logging.info('debut')
    
    dialog = Dialog()
    audio_recorder = AudioRecorder(dialog)
    # face = FaceRecognition(audio_recorder)
    main()
  
    # subprocess.Popen("python3 faceManager.py", shell=True)
    print("fy")
    logging.info('fin')
    