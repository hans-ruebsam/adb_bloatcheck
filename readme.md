# 📦 Android Bloatware-Scanner (ADB-gestützt)

Prototypisches Python-Tool, das installierte Apps auf einem Android-Gerät per ADB ausliest, mit bekannten Bloatware-Listen abgleicht und klassifiziert. Optionaler Export als CSV, JSON oder Markdown.

---

## 🔧 Voraussetzungen

* Windows 11 oder Linux/macOS
* [Python 3.8+](https://www.python.org/downloads/)
* [ADB (Android Debug Bridge)](https://developer.android.com/tools/releases/platform-tools) im `PATH`
* Entwickleroptionen & USB-Debugging auf dem Gerät aktiviert

---

### 📁 Projektstruktur

```bash  
adb_bloatware_scanner/
├── debloat_lists/        # Lokale JSON-Listen (werden automatisch geladen)
├── list_packages.py      # Hauptskript: Paket-Scan und Klassifikation
├── debloat_update.py     # Updater für die JSON-Bloatware-Datenbank
├── requirements.txt      # Optional, leer oder mit `requests`
├── .gitignore            # Git-Konfiguration
└── README.md             # Diese Datei
```

---

### 🚀 Installation

```bash
python -m venv env
.\env\Scripts\activate   # Windows
# oder
source env/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

> Hinweis: Das Tool benötigt keine externen Pakete außer `requests` für den Updater.

---

### 🗂️ Datenbank aktualisieren

Lädt JSON-Dateien aus dem Repository
[github.com/MuntashirAkon/android-debloat-list](https://github.com/MuntashirAkon/android-debloat-list)

```bash
python debloat_update.py
```

Die Daten werden im Verzeichnis `debloat_lists/` abgelegt.

---

### 📋 Pakete analysieren

```bash
python list_packages.py
```

Optional mit Export:

```bash
python list_packages.py --csv pakete.csv --json pakete.json --md pakete.md
```

---

### ⚙️ Argumente

| Parameter      | Beschreibung                        |
| -------------- | ----------------------------------- |
| `--csv DATEI`  | Export als CSV                      |
| `--json DATEI` | Export als JSON                     |
| `--md DATEI`   | Export als Markdown                 |
| `--lists PFAD` | Pfad zum Ordner mit den JSON-Listen |

---

### 📌 Klassifikation

Jedes Paket wird folgendermaßen eingestuft:

* `recommended: true` → Empfohlen zu entfernen (z. B. OneDrive, Facebook-Stub)
* `recommended: false` → Neutral oder systemrelevant
* `category: ...` → Quelle der Empfehlung (`Recommended`, `Optional`, `Unsafe`, etc.)

---

### 🔒 Sicherheit

Dieses Tool **deinstalliert keine Apps automatisch**. Es analysiert und klassifiziert lediglich die installierten Pakete anhand einer vertrauenswürdigen öffentlichen Datenbank.  
