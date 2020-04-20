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
                    if titleSong.lower() == song.lower():
                        print("Perfect match " + lyricsURL)
                    else:
                        print("Could not find the same exact title, lyrics might be wrong " + URL)
                    lyrics = artist + " - " + song + " " + lyricsURL + " " + si.getLyrics(si.getSoup(lyricsURL))
                
            f = open("lyrics.txt", "w+")
            f.write(lyrics)
            f.close()
        else:
            print("No song playing")

        oldWindowTitle = newWindowTitle
        


    sleep(1)