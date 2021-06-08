import sys
import os
import threading
import logging
import subprocess

from dialog import Dialog
from audioManager import AudioRecorder
from faceManager import FaceRecognition
logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)


if __name__ == "__main__":
    logging.info('debut')
    
    dialog = Dialog()
    audio_recorder = AudioRecorder(dialog) #lancer la  reconnaissance vocal
    face = FaceRecognition(audio_recorder) #lancer la  reconnaissance facial
    logging.info('fin')
    #subprocess.Popen("py -3.5 faceManager.py", shell=True)