# BPM Calculator

Script to calculate the BPM of an audio file (mp3, m4a, wav, etc.).

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/download.html) — required for mp3/m4a decoding
  ```bash
  # macOS
  brew install ffmpeg

  # Linux (Debian/Ubuntu)
  sudo apt install ffmpeg

  # Linux (Fedora)
  sudo dnf install ffmpeg

  # Windows
  # Download from https://ffmpeg.org/download.html or via WSL
  ```

## Development

### 1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install pydub librosa numpy scipy
```

### 3. Run the script

```bash
python3 main.py <file_path>
```

Example:

```bash
python3 main.py "track.mp3"
# 🎵 Detected BPM: 128.45
```

## Generate standalone executable

```bash
pip install pyinstaller
pyinstaller --onefile --name bpm-calculator main.py
```

The executable is generated in `dist/bpm-calculator`.

## Notes

- The virtual environment is ignored in git (`.gitignore`).
- `focus_kick=True` (default) filters low frequencies (20-150 Hz) for higher accuracy.
- Without ffmpeg, only native WAV files will work.
