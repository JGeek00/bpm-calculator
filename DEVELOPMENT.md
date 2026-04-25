# Development

Instructions for developers: creating a virtual environment, installing dependencies, running locally and building the standalone executable.

## 1. Create virtual environment

Recommended to use a recent Python (3.12 is recommended on macOS for wheel availability):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run the script locally

```bash
python3 main.py <file_path_or_directory>
```

Example:

```bash
python3 main.py "track.mp3"
# ✅ 128.45 BPM -> track.mp3
```

## 4. Build standalone executable

We provide a helper script `build.sh` that automates venv creation/usage, dependency installation and the PyInstaller build.

Recommended (using the helper script):

```bash
# Run with the system shell (script auto-detects python3.12 when available)
bash build.sh

# Or make it executable and run directly
chmod +x build.sh
./build.sh

# Recreate the venv and force a clean install
./build.sh --recreate-venv

# Specify a Python interpreter (e.g. python3.12)
./build.sh --python python3.12
```

Manual build (alternative):

1. Create and activate venv (see above).
2. Install requirements and PyInstaller:

```bash
pip install -r requirements.txt
pip install pyinstaller==6.20.0
```

3. Build using the project spec (the spec is configured to produce a single-file executable):

```bash
./.venv/bin/pyinstaller --clean bpm-calculator.spec
```

Or, to build from the script directly:

```bash
./.venv/bin/pyinstaller --onefile --clean main.py
```

### Notes and troubleshooting

- `ffmpeg` is not bundled with the executable; install it system-wide (e.g. `brew install ffmpeg` on macOS).
- If the frozen binary raises `ModuleNotFoundError` for packages like `numpy`, rebuild using the same venv where those packages are installed (use `./.venv/bin/pyinstaller` or `build.sh`).
- Building SciPy from source on Python 3.14 can fail if a Fortran compiler is missing (e.g. `gfortran`). On macOS install build tools first:

```bash
brew install gcc pkg-config
```

Then recreate the venv with the target Python and reinstall requirements before building.

## 5. Commit and release

- When ready, commit `bpm-calculator.spec`, `build.sh`, `README.md` and `DEVELOPMENT.md` to the repo.
