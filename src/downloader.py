from pytube import YouTube
import os
import base64

async def ytDownload(url: str, fileType: str = "mp4"):
    if fileType != "mp4" or fileType != "mp3":
        fileType = "mp4"

    # Creates a new video object with the YouTube Class and its url
    video = YouTube(url)

    # If the length of the video exceeds 10 minutes, return
    maxLength = 10 * 60
    if video.length > maxLength:
        return None
        # raise Exception("I cannot download a video longer than 10 minutes :/")

    # Generates a safe name to be used in the path name
    safe_name = base64.urlsafe_b64encode(bytes(video.title, 'utf-8')).decode()
    fileExtension = f".{fileType}"

    # Complicated way to "generate" a path
    path = os.path.join(os.getcwd(), "temp")
    endPath = f"{os.path.join(path, safe_name)}{fileExtension}"

    # If the file already exists just return the video
    if os.path.exists(os.path.join(path, f"{video.title}{fileExtension}")) or os.path.exists(endPath):
        return endPath

    # Checks the disired file format to be downloaded
    if fileType == "mp3" or fileType == "140":

        outfile = video.streams.get_audio_only(140).download(path)
        os.rename(outfile, endPath)
    else:
        
        outfile = video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download(path)
        os.rename(outfile, endPath)

    # IF file is larger than 8mb, remove it. Discord can't send it.
    if (os.path.getsize(endPath) / 1048576) >= 8.0:
        os.remove(endPath)
        raise None

    return endPath


