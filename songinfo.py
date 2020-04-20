import os
import win32gui
import win32api
from time import sleep
from urllib import parse
import bs4 as BS
import requests
import lyricsmaster

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36" }
provider = lyricsmaster.AzLyrics()

def getWindowID():
    windowID = win32gui.FindWindow("Chrome_WidgetWin_0", "Spotify Premium")
    return windowID


def getWindowTitle(windowID):
    windowTitle = win32gui.GetWindowText(windowID)
    if windowTitle == "Spotify Premium": # Spotify opened, but no song playing
        #print("No song playing.")
        return -1
    elif windowTitle == "": # Spotify closed
        print("I can't find Spotify anymore... Please make sure Spotify is running and restart this script.")
        exit()
    else:
        #print(windowTitle)
        return windowTitle


def hasSongChanged(currentTitle, newTitle):
    return currentTitle == newTitle


def initSpotify():
    print("Attempting to find Spotify...")

    while getWindowID() == 0:
        print("Please make sure Spotify is running and no song is currently being played... Next try in 5 seconds.")
        sleep(1)
    
    print("Spotify found !")
    return getWindowID()


def getSongInfo(windowTitle):
    songInfo = windowTitle.split(" - ", 1)
    
    if songInfo[1].find(" - ") != -1:
        songInfo[1] = songInfo[1][:songInfo[1].find(" - ")]
    if songInfo[1].find(" (") != -1:
        songInfo[1] = songInfo[1][:songInfo[1].find(" (")]

    return songInfo


def encodeURL(songString):
    return parse.quote(songString)


def getSearchURL(songString):
    return "https://search.azlyrics.com/search.php?q=" + encodeURL(songString)
    

def getSoup(URL):
    page = requests.get(URL, headers=headers)
    soup = BS.BeautifulSoup(page.content, 'html.parser')

    return soup

def getLyricsURL(soup):
    presoup = soup.find(class_="text-left visitedlyr")
    if presoup == None:
        return -1

    lyricURL = str(presoup)

    lyricURL = lyricURL[ lyricURL.find('<a href="') + 9 : lyricURL.find('" target') ]

    return lyricURL

def getLyrics(soup):
    return provider.extract_lyrics(soup)
