import sys
import pathlib
import warnings
import numpy as np
import scipy.signal as signal
import librosa
from pydub import AudioSegment
from mutagen import File as MutagenFile

# Suppress librosa deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="librosa")

# Fallback for librosa < 0.10.0
try:
    from librosa.feature.rhythm import tempo as get_tempo
except ImportError:
    get_tempo = librosa.beat.tempo

def calculate_bpm(file_path, focus_kick=True):
    """
    Calculate BPM of an audio file (mp3, m4a, wav, etc.)
    focus_kick=True → prioritize low frequencies (kick/bass) for higher accuracy.
    """
    # 1. Decode audio
    audio = AudioSegment.from_file(file_path)
    
    # 2. Convert to mono and numeric array
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape(-1, 2).mean(axis=1)
    sr = audio.frame_rate  # Original sampling rate
    
    # 3. (Optional) Filter low frequencies (20-150 Hz) to focus on the kick
    if focus_kick:
        nyquist = sr / 2
        cutoff = 150.0
        b, a = signal.butter(4, cutoff / nyquist, btype='low')
        low_freq = signal.filtfilt(b, a, samples)
        signal_to_use = low_freq
    else:
        signal_to_use = samples
        
    # 4. Calculate onset envelope
    hop_length = 512  # Balance between speed and accuracy
    onset_env = librosa.onset.onset_strength(
        y=signal_to_use, 
        sr=sr, 
        hop_length=hop_length
    )
    
    # 5. Estimate tempo
    tempo = get_tempo(
        onset_envelope=onset_env,
        sr=sr,
        hop_length=hop_length,
    )

    return float(tempo[0])

def write_bpm_tag(file_path, bpm):
    """Write BPM value to the file's metadata tags."""
    audio = MutagenFile(file_path, easy=True)
    if audio is None:
        return
    audio["BPM"] = str(int(round(bpm)))
    audio.save()

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
