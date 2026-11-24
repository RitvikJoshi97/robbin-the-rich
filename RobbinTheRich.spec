# PyInstaller build spec: `pyinstaller RobbinTheRich.spec`
# Produces dist/RobbinTheRich (Windows/Linux folder) or dist/Robbin The Rich.app (macOS).
import sys

app_name = "RobbinTheRich"
icon = "code/assets/images/icon.png"  # converted to .icns/.ico by Pillow

a = Analysis(
    ["RobbinTheRich.py"],
    pathex=["code"],
    datas=[("code/assets", "code/assets"), ("scores.txt", ".")],
    hiddenimports=["paths", "inGame", "endLevel", "endGameCredits", "mainMenu", "addHighscore"],
    excludes=["tkinter", "matplotlib", "IPython", "pytest"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name=app_name,
    console=False,
    icon=icon,
)
coll = COLLECT(exe, a.binaries, a.datas, name=app_name)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="Robbin The Rich.app",
        icon=icon,
        bundle_identifier="io.github.ritvikjoshi97.robbintherich",
        info_plist={"NSHighResolutionCapable": True, "CFBundleShortVersionString": "1.0.0"},
    )
