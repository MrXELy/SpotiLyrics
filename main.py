# -*- coding :Latin -1 -*

import os
import songinfo as si
from time import sleep
from re import compile

windowID = si.initSpotify()
oldWindowTitle = ""
newWindowTitle = si.getWindowTitle(windowID)

while True:
    newWindowTitle = si.getWindowTitle(windowID)
    if si.hasTitleChanged(newWindowTitle, oldWindowTitle):

        if si.isSongPlaying(newWindowTitle):

            lyrics = si.getLyrics(newWindowTitle)

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

os.system("pause")