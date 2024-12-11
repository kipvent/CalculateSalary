# -*- mode: python ; coding: utf-8 -*-
datas = [
    ("program_icon.ico", "."),
    ("relax_music1.mp3", "."),
    ("relax_music2.mp3", "."),
    ("relax_music3.mp3", "."),
    ("relax_music4.mp3", "."),
    ("relax_background.jpg", "."),
    ("thanks_icon.png", "."),
    ("prev_icon.png", "."),
    ("next_icon.png", "."),
    ("music_on.png", "."),
    ("music_off.png", "."),
]

a = Analysis(
    ['last2.py'],
    pathex=[],
    binaries=[],
    datas=datas,  # Здесь добавляем datas
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='last2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="program_icon.ico",  # Путь указывается строкой
)
