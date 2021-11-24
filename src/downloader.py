from pytube import YouTube
import os
import base64
import ffmpeg

def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()


# TODO: FIXA KLART DET HÄR eller ta bort
def generateFilePath(path, name):
    safe_name = base64.urlsafe_b64encode(bytes(name.title, "utf-8")).decode()

    fileExtension = ""

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
    else:
        outfile = video.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download(path)

    os.rename(outfile, endPath)
    
    # Alternative? https://stackoverflow.com/questions/64430805/how-to-compress-video-to-target-size-by-python (not working properly)
    # IF file is larger than 8mb, remove it. Discord can't send it.
    if (os.path.getsize(endPath) / 1048576) >= 8.0:
        # compress_video(endPath, f"{safe_name}{fileExtension}", 8 * 1000)
        os.remove(endPath)
        return None

    return endPath


