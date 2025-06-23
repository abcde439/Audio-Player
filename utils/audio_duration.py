import subprocess
import shutil
import json

def get_audio_duration(path: str) -> float:
  # Check if ffprobe is available
  if not shutil.which("ffprobe"):
    raise RuntimeError("ffprobe is not installed or not found in PATH.")

  try:
    result = subprocess.run(
      ['ffprobe', '-v', 'error', '-show_entries',
       'format=duration', '-of', 'json', path],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      check=True
    )
  except subprocess.CalledProcessError as e:
    raise RuntimeError(f"ffprobe failed to read the file: {e.stderr.strip()}") from e
  except FileNotFoundError as e:
    raise RuntimeError("ffprobe executable not found.") from e

  try:
    data = json.loads(result.stdout)
    duration = float(data['format']['duration'])
  except (KeyError, ValueError, json.JSONDecodeError) as e:
    raise ValueError("Could not extract duration from ffprobe output.") from e

  return duration
  
if __name__ == "__main__":
  print(get_audio_duration("../test.mp3"))
