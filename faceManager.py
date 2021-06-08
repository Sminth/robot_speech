
import random
import threading
import subprocess
import time,os
from dialog import Dialog
from audioManager import AudioRecorder

from dialog import Dialog

class FaceRecognition(object):
    def __init__(self, audio_recorder):
        """if audio_recorder is None:
            print("none param")
            self.audio_recorder = AudioRecorder(Dialog())
        else :"""
        #self.audio_recorder = AudioRecorder(Dialog())

        self.audio_recorder = audio_recorder
        threading.Thread(target=self.run).start()

    def run(self):
        
        self.detecter = False
  
        self.discute = False
        self.dialog = Dialog()
        self.existe = {}
        self.new=False
        self.unknown_file = {"inconnu":0}
        self.known_file = {"percent":0,"name":"inconnu"}
        self.pre_nom_detecter = ""
        with open("unknown","w") as f : f.write(str(self.unknown_file))
        with open("known","w") as f : f.write(str(self.known_file))
        with open("existe","w") as f : f.write(str(self.existe))
        with open("new","w") as f : f.write(str(self.new))
        threading.Thread(target=lambda: subprocess.Popen("python3 face_system/facerec.py",shell=True)).start()
        self.check_unknown()

        

    def check_unknown(self):
        print("ici")
        
        while True :
            if (self.discute==False) : 
                with open("known", "r") as f :  self.known_file = eval(f.read())
                with open("existe","r") as f : self.existe=eval(f.read())
                self.detecter=self.known_file["percent"]>40
                name=self.known_file["name"]
                # if self.detecter and self.pre_nom_detecter !=name and name not in self.existe: 
                if self.detecter and self.pre_nom_detecter !=name : 
                    self.pre_nom_detecter = self.known_file["name"]
                    self.dialog.SpeakText("Bonjour "+self.pre_nom_detecter)
                    if name not in self.existe : 
                        self.existe[name]=self.detecter
                        with open("existe","w") as f : f.write(str(self.existe))
                    # subprocess.Popen("py -3.5 dialog.py --input \"je suis "+self.known_file["name"]+"\"", shell=True)
                    continue

                with open("unknown","r") as f : self.unknown_file=eval(f.read())
                """if self.unknown_file["inconnu"] > 60 :
                    self.discute=True
                    self.train_model()

                    self.discute=False
                """
            time.sleep(1)

    def train_model(self):
        self.dialog.SpeakText("Bonjour, je ne vous connais pas, quel est votre nom ?")
        time.sleep(3)
        nom =self.audio_recorder.getValue()
        print(nom)
        if nom=="inconnu" or nom =="" or len(nom)<2 :
            self.dialog.SpeakText("desolé je n'est pas saisie votre nom")
        else :
            self.dialog.SpeakText("enchanté "+nom)
            self.take_photo(nom,time.time())

        self.unknown_file ={"inconnu":0}
        with open("unknown","w") as f : f.write(str(self.unknown_file))
        print("entrainement terminé")
    def take_photo(self,nom, date):
        print("enregistrement de "+nom+"\ndate: "+str(date))

#s=FaceRecognition()
