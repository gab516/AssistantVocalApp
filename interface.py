# -*- coding:utf8-*-
from random import randint

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import threading
import time
import AssistantVocal

kivy.require('2.0.0')

enable = False


class Speech_recognizer(threading.Thread):

    def __init__(self):
        super(Speech_recognizer, self).__init__()
        self.recognized_text = None
        self.setDaemon(True)

    # Run assistant
    def run(self):
        welcome = True
        while True:
            if enable:
                if welcome:
                    AssistantVocal.welcome()
                    welcome = False
                time.sleep(0.1)
                request = AssistantVocal.takeCommand()
                print(request)

                if AssistantVocal.name in request and len(request) < len(AssistantVocal.name) + 6:
                    AssistantVocal.pause_music()
                    i = randint(0, 1)
                    if i == 0:
                        AssistantVocal.say("que puis-je faire pour toi")
                    elif i == 1:
                        AssistantVocal.say("oui")

                    request = ""
                    while request == "":
                        request = AssistantVocal.takeCommand()
                        self.recognized_text = request
                        print(request)
                        AssistantVocal.all_command(request)
                    AssistantVocal.pause_music()

                elif AssistantVocal.name in request:
                    AssistantVocal.pause_music()
                    AssistantVocal.all_command(request)
                    AssistantVocal.pause_music()

                if "merci" in request:
                    AssistantVocal.pause_music()
                    i = randint(0, 2)
                    if i == 0:
                        AssistantVocal.say("il y a pas de quoi")
                    elif i == 1:
                        AssistantVocal.say("Avec plaisir")
                    elif i == 2:
                        AssistantVocal.say("a ton service")
                    AssistantVocal.pause_music()


recognizer = Speech_recognizer()
recognizer.start()


class View(BoxLayout):
    def __init__(self):
        super(View, self).__init__()
        Clock.schedule_interval(self.update, 0.1)
        Clock.schedule_interval(self.close, 0.1)

    def update(self, *args):
        self.command_sayed.text = AssistantVocal.get_recognized_text()

        AssistantVocal.set_title_of_the_song(self.title_of_the_song.text)
        AssistantVocal.set_name_of_the_artist(self.name_of_the_artist.text)

        if len(AssistantVocal.get_answer()) > 30:
            text1 = AssistantVocal.get_answer()[0:30]
            text2 = AssistantVocal.get_answer().replace(text1, "")
            text3 = ""
            if len(text2) > 30:
                text3 = text2
                text2 = text2[0:30]
                text3 = text3.replace(text2, "")
            final_text = text1+"\n"+text2+"\n"+text3
            self.answer.text = final_text
        else:
            self.answer.text = AssistantVocal.get_answer()
        if AssistantVocal.get_listening_state():
            self.listening_state.background_color = "#00ff00"
        else:
            self.listening_state.background_color = "#ff0000"

    def close(self, *args):
        if "éteins" in self.command_sayed.text:
            time.sleep(2)
            testApp.stop()

    def start_recognizer(self):
        AssistantVocal.name = self.name_of_assistant.text
        global enable
        enable = True


class TestApp(App):
    def build(self):
        return View()


testApp = TestApp()
testApp.run()
