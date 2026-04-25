# BPM Calculator

Script to calculate the BPM of an audio file (mp3, m4a, wav, etc.).

## Requirements

- Python 3.10+ (required to run from source)
- ffmpeg — required for mp3/m4a decoding
- ffmpeg — required for mp3/m4a decoding
  ```bash
  # macOS
  brew install ffmpeg

  # For other platforms, see https://ffmpeg.org/download.html
  ```

## Usage

# macOS

```bash
# Make executable (if needed)
chmod +x bpm-calculator

# Run against a file or directory
./bpm-calculator /path/to/file_or_directory
```

Optional: move the binary to your PATH for convenience:

```bash
sudo mv bpm-calculator /usr/local/bin/
```
Important notes for end users

- The packaged executable is platform-specific (OS and CPU architecture). Download the correct build for your system.
- `ffmpeg` is required for mp3/m4a decoding and is not bundled with the binary. Install it system-wide (e.g. `brew install ffmpeg` on macOS).
- If you only have the source file `main.py` (not the binary), see [DEVELOPMENT.md](DEVELOPMENT.md) for instructions to create the standalone executable.
