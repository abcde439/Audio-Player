import ctypes
import subprocess

lib_stream = ctypes.CDLL('./player/c/libaudio3.so')
lib_stream.play_stream_fd.argtypes = [ctypes.c_int]
lib_stream.play_stream_fd.restype = None
lib_stream.audio_pause.argtypes = []
lib_stream.audio_pause.restype = None
lib_stream.audio_resume.argtypes = []
lib_stream.audio_resume.restype = None
lib_stream.audio_stop.argtypes = []
lib_stream.audio_stop.restype = None

class YtdlpAudioPlayer():
  def play(self, url: str):
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
    
    if yt_dlp.returncode not in (None, 0):
      raise RuntimeError("yt-dlp failed")
    if ffmpeg.stdout is None:
      raise RuntimeError("ffmpeg stdout is None")

    yt_dlp.stdout.close()
    fd = ffmpeg.stdout.fileno()
    lib_stream.play_stream_fd(fd)
    ffmpeg.wait()
  
  def pause(self):
    lib_stream.audio_pause()
  
  def resume(self):
    lib_stream.audio_resume()
  
  def stop(self):
    lib_stream.audio_stop()