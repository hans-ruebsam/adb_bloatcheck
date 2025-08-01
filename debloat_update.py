import os
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_URL = "https://raw.githubusercontent.com/MuntashirAkon/android-debloat-list/master"
LISTS = ["oem.json", "misc.json", "google.json", "carrier.json", "aosp.json"]
TARGET_DIR = Path("debloat_lists")
MAX_AGE_DAYS = 7  # Aktualisieren, wenn älter als 7 Tage

def download_list(name):
    url = f"{BASE_URL}/{name}"
    local_path = TARGET_DIR / name
    try:
        print(f"Lade {name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Gespeichert: {local_path}")
    except Exception as e:
        print(f"Fehler beim Herunterladen von {name}: {e}")

def is_stale(path):
    if not path.exists():
        return True
    modified = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - modified > timedelta(days=MAX_AGE_DAYS)

def update_all():
    TARGET_DIR.mkdir(exist_ok=True)
    for name in LISTS:
        path = TARGET_DIR / name
        if is_stale(path):
            download_list(name)
        else:
            print(f"{name} ist aktuell.")

if __name__ == "__main__":
    update_all()
