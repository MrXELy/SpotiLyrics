import os
import songinfo as si
from time import sleep

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

            if lyricsURL == -1:
                print("No lyrics ? " + URL)
                lyrics = "Can't find the lyrics... " + URL
            else:    
                lyrics = artist + " - " + song + " " + lyricsURL + " " + si.getLyrics(si.getSoup(lyricsURL))
                
            f = open("lyrics.txt", "w+")
            f.write(lyrics)
            f.close()
        else:
            print("No song playing")

        oldWindowTitle = newWindowTitle
        


    sleep(1)