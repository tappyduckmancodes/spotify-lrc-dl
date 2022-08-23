from re import A
import secrets, requests, base64, os, spotipy, urllib.request, time, json, ast, sys, bs4, selenium, urllib3, itertools, re, shutil, subprocess, platform
from itertools import zip_longest
from sre_constants import SUCCESS
from turtle import clear
import spotipy.util as util
from secrets import *
from pprint import pprint
from os import path
from spotipy.oauth2 import SpotifyOAuth

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls()

try:
    os.remove("timings.txt")
    os.remove('timingsfixed.txt')
    os.remove('timingsfixed.lrc')
except:
    print("\n")

# Authorization for API token
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}
# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')
headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"
r = requests.post(url, headers=headers, data=data)
token = r.json()['access_token']
print(token)
#set up spotipy with token and client ids
os.environ['SPOTIPY_CLIENT_ID']  = clientId
os.environ['SPOTIPY_CLIENT_SECRET'] = clientSecret
os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI
scope = "user-read-currently-playing"
# spotipy authentication to see currently playing song
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope))
current_track = sp.current_user_playing_track()
#print(current_track)
# saves currently playing song info to json file
result = str(current_track) #result is string version if using json stuff fuse current_track

with open("test.json", "w") as outfile:
    json.dump(current_track, outfile) #temp json file for parsing

if (current_track) is None:
    print("No song detected, make sure you're actively playing a song!")
    quit()
else:
    #goes over dict to find specific keys
    with open('test.json', 'r') as json_file:
        data = json.load(json_file)
#dirs
item = (data.get("item"))
album = (item.get("album"))
images = (album.get("images"))
artists = (album.get("artists"))
#items
artist_name = artists[0].get('name')
album_uri = album.get('uri')
artist_uri = artists[0].get('uri')
image_url = images[0].get('url')
album_name = album.get('name')
release_date = album.get('release_date')
song_name = item.get('name')
song_uri = item.get('uri')
song_uri_number = song_uri.replace("spotify:track:", "")
track_number = item.get('track_number')

# getting release year for album
release_date = release_date.replace('-', '/')
release_year = release_date[:4]

print("Success! Song Detected!\n")
print(artist_name)
print(song_name)
print(album_name)
print(artist_uri)
print(album_uri)
print(song_uri)
print("Released in " + release_year)
print(image_url)
print("Track Number: " + str(track_number))

# generate lyrics link
original_link = image_url
a = (image_url)
a = a.replace("/", "%2F")
a = a.replace(":", "%3A")
cover_link = a
link_start = "https://spclient.wg.spotify.com/color-lyrics/v2/track/"
lyrics_url = (link_start + song_uri_number + "/image/" + cover_link + "?format=json&vocalRemoval=false&market=from_token")
lyrics_url_no_access = (link_start + song_uri_number + "/image/" + image_url)
print("\n" + lyrics_url)
json_file.close()


# what this should do (plans)
# open browser to spotify login page
# save cookies and login info
# close browser
# open headless browser with lyric link
# scrape open page copy and verify


headers = {
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'accept-language': 'en',
    'sec-ch-ua-mobile': '?0',
    'authorization': secrets.lyricauthorization,
    'accept': 'application/json',
    'Referer': 'https://open.spotify.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'spotify-app-version': '1.1.93.541.gc6ce4634',
    'app-platform': 'WebPlayer',
    'client-token': secrets.clienttoken,
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'format': 'json',
    'vocalRemoval': 'false',
    'market': 'from_token',
}

response = requests.get(lyrics_url, params=params, headers=headers)
#print(response.content) uncomment to see raw data from website

lyric_json = (response.content)
z = open("lyrics.txt", "wb")
z.write(lyric_json)
z.close()
#print(lyric_json)

if (lyric_json) is None:
    print("No lyrics detected, make sure you're actively playing a song!")
    quit()
else:
    print("SUCCESS!")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# old string-manipulation conversion logic but it works
# Read in the file
with open('lyrics.txt', 'r') as file :
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('},', '} \n')
filedata = filedata.replace('{"lyrics":{"syncType":"LINE_SYNCED","lines":[', '')
filedata = filedata.replace('\\u0027', '\'')
filedata = filedata.replace('{"startTimeMs":"', '[')
filedata = filedata.replace(',"syllables":[]} ', '')
filedata = filedata.replace('","words":', ']')
filedata = filedata.replace('"', '')
filedata = filedata.replace('hasVocalRemoval:false}', '')
filedata = filedata.replace(']', '] ')
# Write the file out again
with open('lyricsfixed.lrc', 'w') as file:
    file.write(filedata)
# remove leftover shit from spotify that doesnt apply to lrc files
with open("lyricsfixed.lrc", "r") as f:
    lines = f.readlines() 
with open("lyricsfixed.lrc", "w") as new_f:
    for line in lines:
        if not line.startswith("colors:{background"):
            new_f.write(line)
# remove last line 
import os, sys, re
readFile = open("lyricsfixed.lrc")
lines = readFile.readlines()
readFile.close()
w = open("lyricsfixed.lrc",'w')
w.writelines([item for item in lines[:-1]])
w.close()
with open('lyricsfixed.lrc', 'r') as file :
    filedata = file.read()
# initializing string
test_str = filedata
# Extract Numbers in Brackets in String
# Using regex
res = re.findall(r"\[\s*\+?(-?\d+)\s*\]", test_str)
# saving to timings.txt
file = open("timings.txt", "w")

corrected_times = []
for time in res:
  corrected_times.append((int(time)) / 1000)

formatted_times = [] #timing conversion
for time in res:
  millis = int((int(time) % 1000) / 10)
  secs = int(int(time) / 1000)
  mins = int(secs / 60)
  secs = secs % 60
  formatted_times.append(f"{mins}:{secs}.{millis}")

text = '] \n'.join(formatted_times) # line breaks
file.write(text)
file.close()

# Read in the file
with open('timings.txt', 'r') as file :
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('0:', '[00:')
filedata = filedata.replace('1:', '[01:')
filedata = filedata.replace('2:', '[02:')
filedata = filedata.replace('3:', '[03:')
filedata = filedata.replace('4:', '[04:')
filedata = filedata.replace('5:', '[05:')
filedata = filedata.replace('6:', '[06:')
filedata = filedata.replace('7:', '[07:')
filedata = filedata.replace('8:', '[08:')
filedata = filedata.replace('9:', '[09:')
filedata = filedata.replace(':0.', ':00.')
filedata = filedata.replace(':1.', ':01.')
filedata = filedata.replace(':2.', ':02.')
filedata = filedata.replace(':3.', ':03.')
filedata = filedata.replace(':4.', ':04.')
filedata = filedata.replace(':5.', ':05.')
filedata = filedata.replace(':6.', ':06.')
filedata = filedata.replace(':7.', ':07.')
filedata = filedata.replace(':8.', ':08.')
filedata = filedata.replace(':9.', ':09.')
filedata = filedata.replace('.9]', '.90]')
filedata = filedata.replace('.8]', '.80]')
filedata = filedata.replace('.7]', '.70]')
filedata = filedata.replace('.6]', '.60]')
filedata = filedata.replace('.5]', '.50]')
filedata = filedata.replace('.4]', '.40]')
filedata = filedata.replace('.3]', '.30]')
filedata = filedata.replace('.2]', '.20]')
filedata = filedata.replace('.1]', '.10]')
filedata = filedata.replace('.0]', '.00]')
with open('timingsfixed.txt', 'w') as file:
    file.write(filedata)

with open('timingsfixed.txt', 'r') as file :
    filedata = file.read()
filedata = filedata.replace('1 ', '1]')
filedata = filedata.replace('2 ', '2]')
filedata = filedata.replace('3 ', '3]')
filedata = filedata.replace('4 ', '4]')
filedata = filedata.replace('5 ', '5]')
filedata = filedata.replace('6 ', '6]')
filedata = filedata.replace('7 ', '7]')
filedata = filedata.replace('8 ', '8')
filedata = filedata.replace('9 ', '9]')

s1 = filedata
s2 = "]"
filedatawithlastbracket = (s1 + s2)

with open('timingsfixed.txt', 'w') as file:
    file.write(filedatawithlastbracket)

os.remove("timings.txt")
#os.rename('timingsfixed.txt', 'timingsfixed.lrc')

with open('lyricsfixed.lrc', 'r') as file :
    filedata = file.read()
# initializing string
test_str = filedata
a_string = test_str
modified_string = re.sub(r"\[\s*\+?(-?\d+)\s*\]", "", a_string)

with open('lyricstimingsremoved.txt', 'w') as file:
    file.write(modified_string)

with open('timingsfixed.txt', 'r') as file :
    filedata = file.read()
with open('lyricstimingsremoved.txt', 'r') as file1:
    test_str = file1.read()

with open('timingsfixed.txt', 'r') as src1, open('lyricstimingsremoved.txt', 'r') as src2, open('output.lrc', 'w') as dst:
    for line_from_first, line_from_second in itertools.zip_longest(src1, src2):
        if line_from_first is not None:
            dst.write(line_from_first)
        if line_from_second is not None:
            dst.write(line_from_second)

with open('output.lrc', 'r') as file :
    filedata = file.read()
filedata = filedata.replace('   ', '')
with open('output.lrc', 'w') as file:
    file.write(filedata)

with open('output.lrc') as f:
    all_lines = f.readlines()
    all_lines = [x.strip() for x in all_lines if x.strip()]
    two_lines = " ".join(x for x in all_lines[:2])
    lines_left = " ".join(x for x in all_lines[2:])

oneline = (two_lines + lines_left)

# Replace the target string
oneline = oneline.replace('[00:00.00] {lyrics:{syncType:UNSYNCED,lines:[ ', '')
oneline = oneline.replace('[00:00.00] ', '')
oneline = oneline.replace('[00:00.0] ', '')
oneline = oneline.replace(',syllables:[] ,endTimeMs:0}', '')
oneline = oneline.replace(")[", ')\n[')
oneline = oneline.replace(' [', '\n[')
oneline = oneline.replace('.[', '.\n[')
oneline = oneline.replace('![', '!\n[')
oneline = oneline.replace('?[', '?\n[')
oneline = oneline.replace('a[', 'a\n[')
oneline = oneline.replace('b[', 'b\n[')
oneline = oneline.replace('c[', 'c\n[')
oneline = oneline.replace('d[', 'd\n[')
oneline = oneline.replace('e[', 'e\n[')
oneline = oneline.replace('f[', 'f\n[')
oneline = oneline.replace('g[', 'g\n[')
oneline = oneline.replace('h[', 'h\n[')
oneline = oneline.replace('i[', 'i\n[')
oneline = oneline.replace('j[', 'j\n[')
oneline = oneline.replace('k[', 'k\n[')
oneline = oneline.replace('l[', 'l\n[')
oneline = oneline.replace('m[', 'm\n[')
oneline = oneline.replace('n[', 'n\n[')
oneline = oneline.replace('o[', 'o\n[')
oneline = oneline.replace('p[', 'p\n[')
oneline = oneline.replace('q[', 'q\n[')
oneline = oneline.replace('r[', 'r\n[')
oneline = oneline.replace('s[', 's\n[')
oneline = oneline.replace('t[', 't\n[')
oneline = oneline.replace('u[', 'u\n[')
oneline = oneline.replace('v[', 'v\n[')
oneline = oneline.replace('w[', 'w\n[')
oneline = oneline.replace('x[', 'x\n[')
oneline = oneline.replace('y[', 'y\n[')
oneline = oneline.replace('z[', 'z\n[')
oneline = oneline.replace('.0]', '.00]')



with open('output.lrc', 'w') as file:
    file.write(oneline)
os.remove("lyricsfixed.lrc")
os.remove("lyricstimingsremoved.txt")
#os.remove("timingsfixed.lrc") 
os.remove("lyrics.txt")

#z = open("lyrics.txt", "w")
#z.write("Lyrics go here!")
#z.close()

# creates directory
artist = artist_name
album = (album_name + " (" + release_year + ")")
song = song_name
track_number = str(track_number)
lyrics = "Lyrics"
host_dir = os.getcwd()

#creates lyrics folder
if os.path.isdir(lyrics):
    os.chdir(lyrics)
    lyricdir = os.getcwd()
else:
    os.mkdir(lyrics)
    os.chdir(lyrics)

#creates artist folder
if os.path.isdir(artist):
    os.chdir(artist)
    artistdir = os.getcwd()
else:
    os.mkdir(artist)
    os.chdir(artist)
    artistdir = os.getcwd()

#creates album folder
if os.path.isdir(album):
    os.chdir(album)
    albumdir = os.getcwd()
else:
    os.mkdir(album)
    os.chdir(album)
    albumdir = os.getcwd()

os.chdir(host_dir)

#set up variables for moving lyric and setting up cover.jpg location
host_folder = host_dir
lyrics = "Lyrics"
artist_name = artist_name
albumdir = albumdir
song = song_name
cover = lyrics_url
originallyricsfile = (host_folder + "\\output.lrc")
movedlyricsfile = (albumdir + "\\" + track_number + ". " + song + ".lrc")
movedcoverjpg = (albumdir + "\\" + "cover.jpg")
search_string = (artist, song)

#checks if cover exists, if not it downloads
os.chdir(albumdir)
try:
    f = open(movedcoverjpg)
    print("Cover already downloaded, skipping download.")
    f.close()
except IOError:
    print("No cover.jpg detected, downloading now")
    cover = original_link
    f = open(movedcoverjpg,'wb')
    f.write(urllib.request.urlopen(cover).read())
    f.close()
    print("Cover downloaded!")

#os.chdir(movedlyricsfile)
#checks if lyric exists, if not it downloads
try:
    f = open(movedlyricsfile)
    print("Lyric already downloaded, skipping download. Enjoy!")
    f.close()
    open_file(albumdir)
    os.remove("timingsfixed.txt")
    os.remove("output.lrc")
    #os.remove("test.json")
    quit()

except IOError:
    print("No lyric detected, downloading now")
    shutil.copyfile((host_dir + "\\" + "output.lrc"), (albumdir + "\\" + track_number + ". " + song + ".lrc"))
    #prints folder where lyric went
    print("\n")
    print("Moved lyric to:")
    print(movedlyricsfile, "\n")
    open_file(albumdir)
    os.remove(host_dir + "\\" + "timingsfixed.txt")
    os.remove(host_dir + "\\" + "output.lrc")