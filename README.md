# AudioCLI

A simple terminal-based audio player that supports both local audio files and online streaming URLs.  
Designed to be minimal, dependency-light, and usable across platforms.

---

## ✨ Features

- Play local audio files (e.g. MP3, WAV, FLAC)
- Stream and play audio directly from supported URLs (e.g. YouTube)
- Pause, resume, and stop playback interactively via command line
- Cross-platform and simple to use

---

## 🚀 Usage

Run from terminal:

    python main.py <file-path-or-url>

Examples:

    python main.py ./music/song.mp3
    python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

---

## 📦 Dependencies

This project is made possible thanks to the following open-source tools and libraries:

- yt-dlp — YouTube and streaming download  
  License: MIT / Unlicense  
  Repository: https://github.com/yt-dlp/yt-dlp

- FFmpeg — Audio decoding and conversion backend  
  License: LGPL / GPL  
  Website: https://ffmpeg.org/

- miniaudio — Lightweight audio playback for Python  
  License: MIT  
  Repository: https://github.com/irmen/pyminiaudio

---

## 📥 Requirements

To run this program, you need:

- Python 3.7 or newer
- yt-dlp installed (Python package):
  
      pip install yt-dlp

- ffmpeg installed and available in your system's PATH
  
      ffmpeg -version

---

## 🔧 Development Notes

This project is currently executed like this:

    python main.py <file-or-url>

We may provide a standalone CLI wrapper in the future for easier use (e.g. `audiocli <url>`).

---

## 🪪 License

This project is free to use, modify, and share under the spirit of open-source freedom.

There is no restriction on commercial or private use, as long as such usage does not violate applicable laws and regulations.

You are encouraged to give credit to the tools and authors involved, and to respect the licenses of the external software listed above.

---

## 👤 Author

This project was created by a member of the open-source community who supports public access to simple, useful software tools.
