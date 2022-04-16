import random

import deezer
import requests
import unidecode


def search_track(TITRE, ARTISTE=''):
    global tracks
    client = deezer.Client()

    if ARTISTE == '' or ARTISTE == ' ':
        track = search(client, "track", TITRE)
        if track == "":
            return False
        print('Done')
        return track.as_dict()['link']

    else:
        artist = search(client, "artist", ARTISTE)
        if artist == "":
            return False
        stop = False
        for i in range(0, len(artist.get_albums())):
            albums = artist.get_albums()[i]
            print(unidecode.unidecode_expect_nonascii(albums.as_dict()['title']))
            tracks = albums.get_tracks()
            for i in range(0, len(tracks)):
                tracks = albums.get_tracks()[i]
                print("          " + tracks.as_dict()['title'].lower())
                if TITRE in tracks.as_dict()['title'].lower():
                    stop = True
                    break
            if stop:
                break

        print('Done')
        return tracks.as_dict()['link']


def search_album(NOM, ARTISTE=''):
    client = deezer.Client()
    albums = search(client, "albums", NOM)
    if albums == "":
        return False

    if ARTISTE == '' or ARTISTE == ' ':
        print('Done')
        return albums[0].as_dict()['link']
    else:
        artist = search(client, "artist", ARTISTE)
        if artist == "":
            return False
        artist = artist[0].as_dict()['name']

        exit_ = True
        i = 0
        while exit_:
            if artist.lower() in albums[i].as_dict()['artist']['name'].lower():
                exit_ = False
            else:
                i += 1
            if i == len(albums):
                print('not found')
                exit_ = False
                i -= 1

        print('Done')
        return albums[i].as_dict()['link']


def get_playlists():
    playlists = []
    rep = requests.get('https://api.deezer.com/user/11628827/playlists')
    playlistsData = rep.json()['data']
    for i in range(0, len(playlistsData)):
        playlists.insert(i, rep.json()['data'][i]['title'])

    return playlists


def play_playlist(name):
    rep = requests.get('https://api.deezer.com/user/11628827/playlists')
    playlistsData = rep.json()['data']
    for i in range(0, len(playlistsData)):
        if name in rep.json()['data'][i]['title'].lower():
            return rep.json()['data'][i]['id']


def play_random_album_from_artist(ARTIST):
    client = deezer.Client()
    artist = client.search_artists(ARTIST)[0]
    album = artist.get_albums()[random.randint(0, len(artist.get_albums()) - 1)]
    return album.as_dict()['link']


def search(client, type_, name):
    if type_ == "track":
        try:
            return client.search(name)[0]
        except IndexError:
            return ""
    elif type_ == "artist":
        try:
            return client.search_artists(name)[0]
        except IndexError:
            return ""
    elif type_ == "album":
        try:
            return client.search_albums()[0]
        except IndexError:
            return ""
    elif type_ == "albums":
        try:
            return client.search_albums()
        except IndexError:
            return ""



if __name__ == '__main__':
    print(play_random_album_from_artist('Nirvana'))
