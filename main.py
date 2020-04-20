import os
import songinfo as si
from time import sleep
from re import compile

regex = compile('[^a-z0-9A-Z]')
windowID = si.initSpotify()
oldWindowTitle = ""
newWindowTitle = si.getWindowTitle(windowID)

while True:
    newWindowTitle = si.getWindowTitle(windowID)
    if si.hasTitleChanged(newWindowTitle, oldWindowTitle):

        if si.isSongPlaying(newWindowTitle):
            artist, song = si.getSongInfo(newWindowTitle)
            print(artist + " - " + song)

            URL = si.getSearchURL(artist + " " + song)

            lyricsURL = si.getLyricsURL(si.getSoup(URL))

            if lyricsURL == None:
                lyrics = "Can't find the lyrics, no results " + URL
                print(lyrics)
            else:
                titleArtist, titleSong = si.getWebSongInfo(si.getSoup(lyricsURL), artist, song) 
                if regex.sub('', titleArtist).lower().find(regex.sub('', artist).lower()) == -1: # remove all non alphanum chars + look for featuring
                    lyrics = "Can't find the lyrics... " + URL
                    print(lyrics)
                else:
                    if regex.sub('', titleSong).lower().find(regex.sub('', song).lower()) != -1: # if song is part of titleSong
                        print("Perfect match " + lyricsURL)
                    else:
                        print("Could not find the same exact title, lyrics might be wrong " + URL)
                    lyrics = titleArtist + " - " + titleSong + " " + lyricsURL + " " + si.getLyrics(si.getSoup(lyricsURL))

            try:   
                f = open("lyrics.txt", "w+", encoding='utf-8-sig')
                f.write(lyrics)
                f.close()
            except UnicodeEncodeError as e:
                print("Can't write the lyrics: ", e)

        else:
            print("No song playing")

        oldWindowTitle = newWindowTitle
        print()
        


    sleep(1)