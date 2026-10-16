from pathlib import Path

source = Path(SPECPATH) / "source"
qss = source / "desktop_messenger" / "ui" / "assets" / "dark.qss"
schema = source / "desktop_messenger" / "database" / "schema.sql"

a = Analysis(
    [str(source / "run_desktop_messenger.py")],
    pathex=[str(source)],
    binaries=[],
    datas=[
        (str(qss), "desktop_messenger/ui/assets"),
        (str(schema), "desktop_messenger/database"),
    ],
    hiddenimports=["PySide6.QtSvg"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="DesktopMessenger",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name="DesktopMessenger")
