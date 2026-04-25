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
