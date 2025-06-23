import ctypes
import subprocess
from player.audio_player import AudioPlayer

lib_local = ctypes.CDLL("./player/c/libaudio2.so")
lib_local.start_audio.argtypes = [ctypes.c_char_p]
lib_local.start_audio.restype = ctypes.c_int 
lib_local.pause_audio.argtypes = []
lib_local.pause_audio.restype = None
lib_local.resume_audio.argtypes = []
lib_local.resume_audio.restype = None
lib_local.stop_audio.argtypes = []
lib_local.stop_audio.restype = None

class LocalAudioPlayer(AudioPlayer):
  def play(self, filename: str):
    c_path = filename.encode('utf-8')
    result = lib_local.start_audio(c_path)
    if result != 0:
      raise RuntimeError(f"start_audio() failed with code {result}")
  
  def pause(self):
    lib_local.pause_audio()
  
  def resume(self):
    lib_local.resume_audio()
  
  def stop(self):
    lib_local.stop_audio()

if __name__ == "__main__":
  player = LocalAudioPlayer()
  player.play("../tes.mp3")
  
  input("Tekan enter untuk pause...")
  player.pause()
  
  input("Tekan enter untuk resume...")
  player.resume()
  
  input("Tekan enter untuk stop...")
  player.stop()
