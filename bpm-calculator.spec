# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all submodules and data files for dependencies
numpy_pkg = collect_submodules('numpy')
scipy_pkg = collect_submodules('scipy')
librosa_pkg = collect_submodules('librosa')
pydub_pkg = collect_submodules('pydub')
mutagen_pkg = collect_submodules('mutagen')

hidden_imports = list(set(
    numpy_pkg + scipy_pkg + librosa_pkg + pydub_pkg + mutagen_pkg
))

# Collect data files (config, c extensions, etc.)
datas = (
    collect_data_files('numpy')
    + collect_data_files('scipy')
    + collect_data_files('librosa')
    + collect_data_files('pydub')
    + collect_data_files('mutagen')
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'setuptools', 'numpy.testing'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='bpm-calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
