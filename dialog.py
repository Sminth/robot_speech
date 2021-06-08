
import requests
import os
import sys
import io
import json
import numpy as np
import logging
import speech_recognition as sr
import pyttsx3 



class Dialog():
    def __init__(self):
        super(Dialog, self).__init__()

        self.userText = ""
        self.machineText = ""

    def process_init(self,text):
        self.set_user_message(text)
        self.process_user_message()
        self.process_machine_message()

    def SpeakText(self,command):
        engine = pyttsx3.init()
        if engine._inLoop:
            engine.endLoop()
        engine = pyttsx3.init()
        engine.say(command)  
        # engine.setProperty('rate',145)
        engine.runAndWait() 
        
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
            self.response = requests.post("http://192.168.252.228:5005/webhooks/rest/webhook",
                            headers=headers, data=data)
        except :
            logging.error("ERROR :connection au serveur rasa impossible ")
            self.SpeakText("je ne suis pas en mesure de vous repondre pour le moment")

    def process_machine_message(self):
        '''lecture de la reponse de la machine'''
        try:
            if json.loads(self.response.text):
                self.textResponse = json.loads(self.response.text)[0]["text"]
                print("reponse rasa: "+self.textResponse)
                self.SpeakText(self.textResponse)
                logging.debug("message Machine : {self.textResponse}")

            else:
                self.SpeakText("je vous ai pas compris")
                logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")
        except :
            #self.SpeakText("je vous ai pas compris")
            logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")

if __name__ == "__main__":
    arg =sys.argv
    if(len(arg)==3 and arg[1]=="--input"):
        print("argument : "+arg[2])
        input = arg[2]
        d=Dialog()
        d.process_init(input)
        # for i, arg in enumerate(arg):
        #     print("Argument"+str(i)+":"+str(arg))
