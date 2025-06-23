import sys
import os
import signal
import threading
import time
from player.controller import PlayerController
from player.audio_player import AudioPlayer
from player.local_player import LocalAudioPlayer
from player.ytdlp_player import YtdlpAudioPlayer
from utils.audio_duration import get_audio_duration
from utils.network import is_valid_https

# Shared state
controller = PlayerController()

# handle input
def user_input_listener(player: AudioPlayer):
  while controller.running:
    try:
      user = input(":").strip().lower()
    except KeyboardInterrupt:
      handle_exit(player)
    if user == "p":
      controller.pause()
      player.pause()
      print("Paused.")
    elif user == "r":
      controller.resume()
      player.resume()
      print("Resumed.")
    elif user in ("q", "s"):
      controller.stop()
      player.stop()
      print("Stopped by user.")
      break
    else:
      print("Invalid input.")

def run_playback(player, path):
  duration = get_audio_duration(path)
  print(f"Playing: {path} ({duration:.2f} seconds)")
  print("Input (p = pause, r = resume, q = quit)")

  def handle_exit_signal(signum, frame):
    print("\nStopping playback...")
    try:
      player.stop()
    except:
      pass
    sys.exit(0)

  signal.signal(signal.SIGINT, handle_exit_signal)
  signal.signal(signal.SIGTERM, handle_exit_signal)

  # Mulai input listener
  threading.Thread(target=lambda: user_input_listener(player), daemon=True).start()

  # Mulai playback
  player.play(path)
  start_time = time.time()

  # Tunggu sampai durasi tercapai
  try:
    while (time.time() - start_time) < duration and controller.running:
      time.sleep(0.1)
  except KeyboardInterrupt:
    handle_exit_signal(None, None)

  print("Playback finished.")

def main():
  if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--h", "--help", "-help"):
    print("Usage: python main.py <path-or-url>")
    return

  path = sys.argv[1]
  if os.path.exists(path):
    player = LocalAudioPlayer()
    duration = get_audio_duration(path)
    
    run_playback(player, path)
    # print(f"Playing: {path} ({duration:.2f} Seconds)")
    # print("Input (p = pause, r = resume, q = quit)")
  
    # # Handle SIGINT
    # signal.signal(signal.SIGINT, handle_exit)
    # signal.signal(signal.SIGTERM, handle_exit)
  
    # # Start audio playback
    # player.play(path)
    # start_time = time.time()
  
    # # Start input thread
    # threading.Thread(target=lambda:user_input_listener(player), daemon=True).start()

    # print("Program exited.")
  elif is_valid_https(path):
    player = YtdlpAudioPlayer()
    print(f"Playing: {path}")
    print("Input (p = pause, r = resume, q = quit)")
    print("Wait...")

    run_playback(player, path)
    # Handle SIGINT
    # signal.signal(signal.SIGINT, handle_exit)
    # signal.signal(signal.SIGTERM, handle_exit)

    # t = threading.Thread(target=lambda:player.play(path))
    # t.start()
    
    # threading.Thread(target=lambda:user_input_listener(player), daemon=True).start()
    
    # t.join()
    # print("Program exited.")
  else:
    print("Error: file not found")

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("dibatalkan oleh user.")
  except Exception as e:
    print(e)
    sys.exit(1)