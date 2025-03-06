# -*- mode: python ; coding: utf-8 -*-

added_files = [
         ( 'config.json', '.'),
         ]


a = Analysis(
    ['amuse_ui.py'],
    pathex=[],
    binaries=[("./amuseLib/ffmpeg_darwin", "./amuseLib")],
    datas=added_files,
    hiddenimports=["config", "yt_dlp"],
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
    [],
    exclude_binaries=True,
    name='aMuseMent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='aMuseMent',
)
app = BUNDLE(
    coll,
    name='aMuseMent.app',
    icon=None,
    bundle_identifier=None,
)
