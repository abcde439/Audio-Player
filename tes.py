import ctypes
import subprocess

# Load shared library
lib = ctypes.CDLL('./libaudio3.so')

# Set argument dan return type
lib.play_stream_fd.argtypes = [ctypes.c_int]
lib.play_stream_fd.restype = None

lib.audio_pause.argtypes = []
lib.audio_pause.restype = None

lib.audio_resume.argtypes = []
lib.audio_resume.restype = None

lib.audio_stop.argtypes = []
lib.audio_stop.restype = None

def play_from_ytdlp(url: str):
    yt_dlp = subprocess.Popen(
        [
            "yt-dlp",
            "-f", "bestaudio[ext=m4a]/bestaudio",
            "--quiet",
            "--no-warnings",
            "-o", "-",
            url
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-i", "pipe:0",
            "-f", "s16le",
            "-ac", "1",
            "-ar", "22050",
            "-"
        ],
        stdin=yt_dlp.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    yt_dlp.stdout.close()  # penting untuk pipeline

    fd = ffmpeg.stdout.fileno()

    # Panggil fungsi C yang akan memutar audio dari stream PCM
    lib.play_stream_fd(fd)

    ffmpeg.wait()
    
from threading import Thread
import time

def main():
    t = Thread(target=lambda: play_from_ytdlp("https://youtu.be/5r8pv2xJ8QQ"))
    t.start()

    time.sleep(60)
    print("Pausing...")
    lib.audio_pause()

    time.sleep(3)
    print("Resuming...")
    lib.audio_resume()

    time.sleep(5)
    print("Stopping...")
    lib.audio_stop()

    t.join()

main()