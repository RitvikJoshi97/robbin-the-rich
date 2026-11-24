"""Where the game reads assets and keeps the high-score file.

Running from source, everything is relative to the repository root, as before.
In a packaged build (PyInstaller), assets live inside the bundle, which is
read-only, so the high-score file goes in a per-user folder instead.
"""
import os
import shutil
import sys

FROZEN = getattr(sys, "frozen", False)

if FROZEN:
    BASE_DIR = sys._MEIPASS
    DATA_DIR = os.path.join(os.path.expanduser("~"), ".robbin-the-rich")
    os.makedirs(DATA_DIR, exist_ok=True)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = BASE_DIR

SCORES_FILE = os.path.join(DATA_DIR, "scores.txt")

if not os.path.exists(SCORES_FILE):
    bundled = os.path.join(BASE_DIR, "scores.txt")
    if FROZEN and os.path.exists(bundled):
        shutil.copyfile(bundled, SCORES_FILE)
    else:
        with open(SCORES_FILE, "w") as f:
            f.write("username,score\n")
