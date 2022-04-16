import datetime
import time
import webbrowser
import re

import pyautogui
import pyttsx3
import speech_recognition as sr
import unidecode
import wikipedia

import searchDeezer

name = 'Laura'

engine = pyttsx3.init()
voices = engine.getProperty('voice')
engine.setProperty('voice', voices[4])
engine.setProperty('rate', 250)
engine.setProperty('volume', 1)

wikipedia.set_lang('fr')

recognized_text = ""
listening_state = False
answer = ""

title_of_the_song = ""
name_of_the_artist = ""


def get_listening_state():
    return listening_state


def get_recognized_text():
    return recognized_text


def get_answer():
    return answer


def set_title_of_the_song(title):
    global title_of_the_song
    title_of_the_song = title


def set_name_of_the_artist(name):
    global name_of_the_artist
    name_of_the_artist = name


def welcome():
    global name
    if name != "":
        say("bonjour, je suis " + name + ", que puis-je faire pour toi ")
    while name == "":
        say("Bonjour, je suis ton assistant vocal. Comment veux tu m'appeler")
        name = takeCommand()
        print(name)
        say("je m'appelle " + name)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        global listening_state
        listening_state = True
        print("listening")
        audio = r.listen(source)
        listening_state = False

        try:
            print("recognizing")
            text = r.recognize_google(audio, language='fr-FR')
            global recognized_text
            recognized_text = text
            return text
        except Exception:
            return ""


def say(text):
    global answer
    answer = text
    engine.say(text)
    engine.runAndWait()


def reformrequest(query):
    query = str(query)
    if "recherche" in query:
        query = query.replace("recherche", "")
    if "cherche" in query:
        query = query.replace("cherche", "")
    if "sur" in query:
        query = query.replace("sur", "")
    if "wikipedia" in query:
        query = query.replace("wikipedia", "")
    if "internet" in query:
        query = query.replace("internet", "")

    return query


def play_music(type_, titre, artiste=''):
    if type_ == "track":
        say("Recherche de la musique")
        query = searchDeezer.search_track(titre, artiste)
        if not query:
            return False
        webbrowser.open(query)
        time.sleep(6)
        pyautogui.click(400, 530, button="left")
    elif type_ == "album":
        print("Recherche de l'album")
        query = searchDeezer.search_album(titre, artiste)
        if not query:
            return False
        webbrowser.open(query)
        time.sleep(6)
        pyautogui.click(400, 450, button="left")
    elif type_ == "artist":
        print("Recherche de l'album")
        query = searchDeezer.play_random_album_from_artist(artiste)
        if not query:
            return False
        webbrowser.open(query)
        time.sleep(6)
        pyautogui.click(400, 450, button="left")
    elif type_ == "playlist":
        say("Recherche de la playliste")
        webbrowser.open("https://www.deezer.com/fr/playlist/" + str(searchDeezer.play_playlist(titre)))
        time.sleep(6)
        pyautogui.click(690, 430, button="left")


def search_music():
    type_ = ""
    while type_ == "":
        say("Veux tu écouter une musique seulement ou un album ?")
        type_ = unidecode.unidecode_expect_nonascii(takeCommand().lower())
        print(type_)
    if 'titre' in type_ or 'musique' in type_:
        titre = ""
        while titre == "":
            say("Quel titre veux tu écouter ?")
            titre = unidecode.unidecode_expect_nonascii(takeCommand().lower())
            print(titre)

        say("Utiliser le nom d'un artiste augmente la précision de la recherche. Veux tu m'en donner un ?")
        haveAnArtist = unidecode.unidecode_expect_nonascii(takeCommand().lower())
        print(haveAnArtist)
        if 'oui' in haveAnArtist:
            say("Quel est le nom de cet artiste ?")
            artiste = unidecode.unidecode_expect_nonascii(takeCommand().lower())
            print(artiste)
        else:
            artiste = ""

        return "track", titre, artiste

    elif 'album' in type_:
        nom = ""
        while nom == "":
            say("Quel album veux tu écouter ?")
            nom = unidecode.unidecode_expect_nonascii(takeCommand().lower())
            print(nom)

        say("Utiliser le nom d'un artiste augmente la précision de la recherche. Veux tu m'en donner un ?")
        haveAnArtist = unidecode.unidecode_expect_nonascii(takeCommand().lower())
        print(haveAnArtist)
        if 'oui' in haveAnArtist:
            say("Quel est le nom de cet artiste ?2")
            artiste = unidecode.unidecode_expect_nonascii(takeCommand().lower())
            print(artiste)
        else:
            artiste = ""

        return "album", nom, artiste

    else:
        return None, None, None


def stop_music():
    for i in range(0, 2):
        pyautogui.hotkey('ctrl', 'w')


def pause_music():
    pyautogui.press(' ')


def all_command(request):
    request = unidecode.unidecode_expect_nonascii(request.lower())
    print(request)
    global name
    while unidecode.unidecode_expect_nonascii(name.lower()) in request:
        waste, request = request.split(unidecode.unidecode_expect_nonascii(name.lower()))
    if request == "":
        say("je n'ai pas compris, re-essaye.")
    elif "eteins" in request:
        say("d'accord, a bientot")
        return False

    elif "annuler" in request:
        say("Annulation de la prise de la commande.")

    elif "changer" in request and "nom" in request:
        say("Articule en disant mon nouveau nom.")
        name = unidecode.unidecode_expect_nonascii(takeCommand().lower())
        print(name)
        say("Mon nom a bien été changé.")

    ###############
    elif "volume" in request and "assistant" in request \
            or "son" in request and "assistant " in request:
        if any(chr.isdigit() for chr in request):
            volume = re.findall('\d+', request)
            engine.setProperty('volume', float(int(volume[0]) / 100.0))
            say("Le volume de l'assistant a ete mis a " + volume[0] + " pourcent.")
    elif "volume" in request and "principal" in request \
            or "son" in request and "principal" in request:
        if any(chr.isdigit() for chr in request):
            volume = re.findall('\d+', request)
            # speakerDriver.SetMasterVolumeLevel (0.2, 0.0)
            say("Le volume pricipal a ete mis a " + volume[0] + " pourcent.")

    ###############
    elif "heure" in request:
        hour = int(datetime.datetime.now().hour)
        minute = int(datetime.datetime.now().minute)
        if hour == 21:
            say("il est" + str(hour).replace("21", "20 t une") + "heure" + str(minute))
        else:
            say("il est" + str(hour) + "heure" + str(minute))

    ###############
    elif "wikipedia" in request:
        say("recherche de la page wikipedia")
        request = reformrequest(request)
        print(request)
        try:
            results = wikipedia.summary(request, sentences=5)
            url = wikipedia.page(request).url
            say("Page wikipedia trouvée.")
            say(results)
            print(url)
            say("Plus d'information en suivant le lien donner dans la console.")
            global answer
            answer = url
        except:
            say("Page non trouvable, essaye de l'appeler autrement.")

    ###############

    elif "quelles" in request and "playlist" in request:
        say("Les playliste du compte lakasacour sont :")
        for i in range(0, len(searchDeezer.get_playlists())):
            say(searchDeezer.get_playlists()[i])
    elif "mets" in request and "musique" in request:
        if "ecris" in request:
            play_music("track", title_of_the_song, name_of_the_artist)
        else:
            type_, titre, artiste = search_music()
            play_music(type_, titre, artiste)
    elif "mets" in request and "playlist" in request \
            or "joue" in request and "playlist" in request:
        if "ecrit" in request:
            request = title_of_the_song
        else:
            request = request.rsplit(None, 1)[-1]

        play_music("playlist", request)
    elif "mets" in request and "artiste" in request \
            or "mais" in request and "artiste" in request:

        if "ecrit" in request:
            play_music("artist", "", name_of_the_artist)
        else:
            request = request.replace(unidecode.unidecode_expect_nonascii(name.lower()), "")
            request = request.replace(" mets ", "")
            request = request.replace(" mais ", "")
            words = request.split()
            if words[len(words) - 2] == "l'artiste":
                artiste = words[len(words) - 1]
            else:
                artiste = words[len(words) - 2] + " " + words[len(words) - 1]
            request = request.replace(" de l'artiste ", " ")
            titre = request.replace(artiste, "")
            artiste = artiste.replace(" ", "")
            print(titre)
            print(artiste)
            play_music("track", titre, artiste)
    elif "mets du" in request:
        request = request.replace(unidecode.unidecode_expect_nonascii(name.lower()), "")
        request = request.replace(" mets du ", "")
        print(request)
        play_music("artist", "", request)
    elif "mets" in request or "mais" in request:
        request = request.replace(unidecode.unidecode_expect_nonascii(name.lower()), "")
        request = request.replace(" mets ", "")
        request = request.replace(" mais  ", "")
        play_music("track", request)
    elif "pause" in request and "musique" in request or "relance" in request and "musique" in request:
        pause_music()
    elif "stoppe" in request and "musique" in request or "arrete" in request and "musique" in request:
        stop_music()

    ###############
    elif "ou" in request:
        say("Dans ton cul.")

    ###############
    else:
        say("Cette commande n'est pas attribuée. Pour tout ajout ou modification de commande, veuillez "
            "contacter Gabriel.")
    return True
