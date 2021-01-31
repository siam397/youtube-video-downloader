import json

import shutil
import string
from ctypes import windll
from moviepy.editor import *
from pytube import YouTube
from sanitize_filename import sanitize
from youtube_search import YoutubeSearch
from pytube import Playlist


def format_url(url):
    finalurl = url
    mainLink = "https://www.youtube.com"
    if mainLink not in url:
        results = YoutubeSearch(url, max_results=1).to_json()
        results = json.loads(results)
        suffix = results["videos"][0]["url_suffix"]
        finalurl = mainLink + suffix
    return finalurl


def format_path(path):
    if path == "":
        print("*default path is the last drive")
        return ""
    final_path = path.capitalize()
    if "/" in final_path:
        final_path = final_path.replace("/", "\\")
    if final_path[len(final_path) - 1] == "\\":
        lst = list(final_path)
        lst[len(lst) - 1] = ""
        final_path = "".join(lst)
    if not os.path.exists(final_path):
        os.mkdir(final_path)
    return final_path


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def process_download_video(url, path, type):
    while url == "":
        print("url cant be empty")
        url = input("*Paste the link here:")
    print("Downloading...")

    if "mp4" in type or type == "":
        if path == "":
            video = YouTube(url)
            name = video.title
            name = sanitize(name)
            lst = get_drives()
            drive = lst[len(lst) - 1]
            downloaded_video = video.streams.get_highest_resolution().download()
            file = r"" + drive + ":\\" + name + ".mp4"
            shutil.move(downloaded_video, file)

            return "Video downloaded: " + file
        else:
            try:
                video = YouTube(url)
                name = video.title
                name = sanitize(name)
                lst = get_drives()
                downloaded_video = video.streams.get_highest_resolution().download()
                file = r"" + path + "\\" + name + ".mp4"
                shutil.move(downloaded_video, file)

                return "Video downloaded: " + file
            except:
                print("invalid folder name")
                return

    else:
        if path == "":
            video = YouTube(url)
            name = video.title
            name = sanitize(name)
            lst = get_drives()
            drive = lst[len(lst) - 1]
            downloaded_video = video.streams.get_highest_resolution().download()
            clip = VideoFileClip(downloaded_video)
            mp3 = downloaded_video.split(".mp4", 1)[0] + f".{type}"
            audio_clip = clip.audio
            audio_clip.write_audiofile(mp3, verbose=False, logger=None)
            audio_clip.close()
            clip.close()
            os.remove(downloaded_video)
            file = r"" + drive + ":\\" + name + f".{type}"
            shutil.move(mp3, file)

            return "Audio downloaded: " + file
        else:
            try:
                video = YouTube(url)
                name = video.title
                name = sanitize(name)
                lst = get_drives()
                downloaded_video = video.streams.get_highest_resolution().download()
                clip = VideoFileClip(downloaded_video)
                mp3 = downloaded_video.split(".mp4", 1)[0] + f".{type}"
                audio_clip = clip.audio
                audio_clip.write_audiofile(mp3, verbose=False, logger=None)
                audio_clip.close()
                clip.close()
                os.remove(downloaded_video)
                file = r"" + path + "\\" + name + f".{type}"
                shutil.move(mp3, file)

                return "Audio downloaded: " + file
            except:
                print("invalid folder name")
                return


print("type /reset at any point to reset your input\n")
print("type /quit at any point to quit\n")
print("Every input other than the link can be empty\n")
run = True
while run:
    # declare url
    mainLink = "https://www.youtube.com"
    url = input("Type the name of the video or paste the link here: ")
    if "/reset" in url:
        continue
    if "/quit" in url:
        run = False
        break
    url = format_url(url)

    # declare path
    path = input("Type the directory: ")
    if "/reset" in path:
        continue
    if "/quit" in path:
        run = False
        break
    path = format_path(path)

    # declare filetype
    fileType = input("mp3 or wav or mp4?: ")
    if "/reset" in fileType:
        continue
    if "/quit" in fileType:
        run = False
        break
    if fileType == "":
        print("*default format is mp4")

    if "list" in url and mainLink in url:
        playlist = Playlist(url)
        print("wait while the playlist downloads")
        for link in playlist.video_urls:
            process_download_video(link, path, fileType)
            print(f"Downloaded f{playlist.video_urls.index(link) + 1} out of f{len(playlist.video_urls)}")
        print("playlist downloaded")

    else:
        print(process_download_video(url, path, fileType))
    print("\n\n")