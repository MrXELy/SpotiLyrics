# -*- coding :Latin -1 -*

import os
import win32gui
from time import sleep
from urllib import parse
import bs4 as BS
import requests
from re import compile
import unidecode

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36" }

def getWindowID():
    windowID = win32gui.FindWindow("Chrome_WidgetWin_0", "Spotify Premium")
    return windowID


def isSongPlaying(windowTitle):
    return not(windowTitle == "Spotify Premium" or windowTitle == "Spotify" or windowTitle == "Spotify Free")


def getWindowTitle(windowID):
    windowTitle = win32gui.GetWindowText(windowID)

    if windowTitle == "": # Spotify closed
        print("I can't find Spotify anymore... Please make sure Spotify is running and restart this script.")
        exit()

    return windowTitle


def hasTitleChanged(currentTitle, newTitle):
    return not(currentTitle == newTitle)


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
        return None

    lyricURL = str(presoup)

    lyricURL = lyricURL[ lyricURL.find('<a href="') + 9 : lyricURL.find('" target') ]

    return lyricURL


def getWebSongInfo(soup, artist, song):
    webTitle = soup.find("title").get_text()

    if webTitle.find("Paroles de") != -1: # French
        titleArtist, titleSong = webTitle.split(" - ", 1)
        titleSong = titleSong[ titleSong.find(' "') + 2 : titleSong.find('" |') ]
    elif webTitle.find("Letra de") != -1: # Spanish
        titleArtist, titleSong = webTitle.split(" - ", 1)
        titleSong = titleSong[ titleSong.find(' "') + 2 : titleSong.find('" |') ]
    else:
        titleArtist, titleSong = webTitle.split(" - ", 1)
        titleSong = titleSong[ 0 : titleSong.find(' Lyrics') ]

    return titleArtist, titleSong


def extractLyrics(URL): #AZLyrics
    soup = getSoup(URL)

    text = str(soup.find(class_="col-xs-12 col-lg-8 text-center"))
    text = text[ text.find(" -->") + 5 : ]
    text = text[ : text.find("</div>") ]
    regex = compile('<[^>]*>')
    text = regex.sub('', text)
    return text


def getGeniusURL(artist, song):
    regex = compile('[^a-zA-Z0-9 ]+')

    artist = unidecode.unidecode(artist)
    artist = artist.replace("&", "and")
    artist = regex.sub('', artist)
    artist = artist.replace(" ", "-")
    
    song = unidecode.unidecode(song)
    song = regex.sub('', song)
    song = song.replace(" ", "-")

    URL = f'https://genius.com/{artist}-{song}-lyrics'

    return URL


def extractGeniusLyrics(URL):
    soup = getSoup(URL)

    lyrics = soup.find("div", class_="lyrics").get_text()
    
    return lyrics


def getLyrics(windowTitle):
    regex = compile('[^a-z0-9A-Z]')

    artist, song = getSongInfo(windowTitle)
    print(artist + " - " + song)
    URL = getSearchURL(artist + " " + song)

    lyricsURL = getLyricsURL(getSoup(URL))

    if lyricsURL == None:
        lyrics = "Can't find the lyrics, no results " + URL
        print(lyrics)
    else:
        titleArtist, titleSong = getWebSongInfo(getSoup(lyricsURL), artist, song)
        if regex.sub('', titleArtist).lower().find(regex.sub('', artist).lower()) == -1: # remove all non alphanum chars + look for featuring
            lyrics = "Can't find the lyrics... " + URL
            print(lyrics)
        else:
            if regex.sub('', titleSong).lower().find(regex.sub('', song).lower()) != -1: # if song is part of titleSong
                print("Perfect match " + lyricsURL)
            else:
                print("Could not find the same exact title, lyrics might be wrong " + URL)
            lyrics = titleArtist + " - " + titleSong + " " + lyricsURL + " " + '\n\n' + extractLyrics(lyricsURL)

    return lyrics