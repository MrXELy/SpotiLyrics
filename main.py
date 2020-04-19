import os
from songinfo import *

windowID = initSpotify()
windowTitle = getWindowTitle(windowID)

while 1:
    windowTitle = getWindowTitle(windowID)
    if windowTitle != -1:
        artist, song = getSongInfo(windowTitle)

        URL = searchURL(artist + " " + song)

        lyricsURL = hasLyrics(getSoup(URL))

        if lyricsURL == False:
            print("No lyrics ? " + URL)
            lyrics = "Can't find the lyrics... "
        else:    
            lyrics = artist + " - " + song + " " + lyricsURL + " " + getLyrics(getSoup(lyricsURL))
            
        f = open("lyrics.txt", "w+")
        f.write(lyrics)

    sleep(1)



 