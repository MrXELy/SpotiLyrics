import os
import songinfo as si
from time import sleep

windowID = si.initSpotify()
windowTitle = si.getWindowTitle(windowID)

while 1:
    windowTitle = si.getWindowTitle(windowID)
    if windowTitle != -1:
        artist, song = si.getSongInfo(windowTitle)

        URL = si.searchURL(artist + " " + song)

        lyricsURL = si.hasLyrics(si.getSoup(URL))

        if lyricsURL == False:
            print("No lyrics ? " + URL)
            lyrics = "Can't find the lyrics... "
        else:    
            lyrics = artist + " - " + song + " " + lyricsURL + " " + si.getLyrics(si.getSoup(lyricsURL))
            
        f = open("lyrics.txt", "w+")
        f.write(lyrics)

    sleep(1)



 