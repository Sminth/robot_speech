
import requests
import os,time
import sys
import io
import json
import numpy as np
import logging
import speech_recognition as sr
import pyttsx3 
import queue,threading


class Dialog():
    def __init__(self):
        super(Dialog, self).__init__()

        self.userText = ""
        self.machineText = ""
        self.en_lecture = False
        self.attente = queue.Queue(3)
        self.attente_isplein=self.attente.full()
        threading.Thread(target=self.speak).start()

    def add_file_attente(self,item):
        self.attente_isplein=self.attente.full()
        if self.attente_isplein : return 
        self.attente.put(item)

    def speak(self):
        while True:
            n=self.attente.qsize()
            if n==0 : pass
            else : 
                for i in range(n):
                    self.SpeakText(self.attente.get())

    def process_init(self,text):
        # AudioRecorder().pause=True
        print("process fpour : "+str(text))
        self.set_user_message(text)
        self.process_user_message()
        self.process_machine_message()
        print("fin process pour : "+str(text))
        return
        # AudioRec  order().pause=False
        
    def SpeakText(self,command):
        self.en_lecture = True
        engine = pyttsx3.init()
        if engine._inLoop:
            engine.endLoop()
        engine = pyttsx3.init()
        engine.say(command)  
        engine.runAndWait() 
        self.en_lecture = False
    def process_user_message(self):
        ''' envoie du message du user a la machine'''
        
        self.send_user_msg_to_chatbot(self.userText)
        logging.debug("message user : {self.textResponse}")

    def set_user_message(self, string):
        self.userText = string

    def send_user_msg_to_chatbot(self, message):
        
        try :
            headers = {"Content-type": "application/json"}
            data = "{\"sender\": \"user1\", \"message\": \" " + message + "\"}"
            tps1 = time.time()        
            self.response = requests.post("http://192.168.252.228:5005/webhooks/rest/webhook",
                            headers=headers, data=data)

            print("temps de reponse rasa : "+str(time.time()-tps1)+" seconde")

        except :
            logging.error("ERROR :connection au serveur rasa impossible ")
            if self.attente_isplein : return 
            else : self.add_file_attente("je ne suis pas en mesure de vous repondre pour le moment")
            # self.SpeakText("je ne suis pas en mesure de vous repondre pour le moment")

    def process_machine_message(self):
        '''lecture de la reponse de la machine'''
        try:
            if json.loads(self.response.text):
                self.textResponse = json.loads(self.response.text)[0]["text"]
                print(self.textResponse)
                if self.attente_isplein : return 
                self.add_file_attente(self.textResponse)
                # self.SpeakText(self.textResponse)
                logging.debug("message Machine : {self.textResponse}")
                return
            else:
                #self.SpeakText("je vous ai pas compris")
                logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")
        except :
            # self.SpeakText("je vous ai pas compris")
            logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")

if __name__ == "__main__":
    arg =sys.argv
    if(len(arg)==3 and arg[1]=="--input"):
        print("argument : "+arg[2])
        entre = arg[2]
        d=Dialog()
        d.process_init(entre)
        
        # for i, arg in enumerate(arg):
        #     print("Argument"+str(i)+":"+str(arg))
