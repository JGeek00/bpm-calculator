import sys
import pathlib

from bpm import calculate_bpm, write_bpm_tag

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff", ".aif", ".opus", ".webm"}


def is_audio_file(path):
    return path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bpm-calculator.py <file_path | directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    path = pathlib.Path(input_path)

    if path.is_dir():
        audio_files = [p for p in path.rglob("*") if is_audio_file(p)]
        if not audio_files:
            print(f"No audio files found in {input_path}")
            sys.exit(1)
        for file_path in sorted(audio_files):
            file_name = file_path.name
            try:
                bpm = calculate_bpm(str(file_path))
                write_bpm_tag(str(file_path), bpm)
                print(f"✅ {bpm:.2f} BPM -> {file_name}")
            except Exception as e:
                print(f"❌ {e}")
    else:
        file_name = input_path.split("/")[-1]
        try:
            bpm = calculate_bpm(input_path)
            write_bpm_tag(input_path, bpm)
            print(f"✅ {bpm:.2f} BPM -> {file_name}")
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)
