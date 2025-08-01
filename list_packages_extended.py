import subprocess
import json
import csv
import argparse
from pathlib import Path

def get_installed_packages():
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages"],
            capture_output=True,
            text=True,
            check=True
        )
        return [line.replace("package:", "").strip() for line in result.stdout.splitlines()]
    except subprocess.CalledProcessError as e:
        print("ADB-Befehl fehlgeschlagen:", e)
        return []
    except FileNotFoundError:
        print("ADB wurde nicht gefunden. Bitte prüfe, ob ADB im PATH ist.")
        return []

def load_combined_bloatware_db(directory: Path) -> dict:
    result = {}
    for file in directory.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                entries = json.load(f)
                for entry in entries:
                    pkg = entry.get("package")
                    if not pkg:
                        continue
                    result[pkg] = {
                        "name": entry.get("description", "-"),
                        "category": entry.get("category", "unknown"),
                        "recommended": entry.get("category", "").lower() in ["recommended", "safe"]
                    }
        except Exception as e:
            print(f"Fehler beim Lesen von {file.name}: {e}")
    return result

def classify_packages(installed, database):
    result = []
    for pkg in installed:
        entry = database.get(pkg, None)
        if entry:
            result.append({
                "package": pkg,
                "name": entry.get("name", "-"),
                "category": entry.get("category", "-"),
                "recommended": entry.get("recommended", False)
            })
        else:
            result.append({
                "package": pkg,
                "name": "-",
                "category": "unbekannt",
                "recommended": False
            })
    return result

def print_table(data):
    print(f"{'Package':<50} {'Kategorie':<15} {'Name':<30} {'Empf.'}")
    print("-" * 100)
    for entry in data:
        print(f"{entry['package']:<50} {entry['category']:<15} {entry['name']:<30} {str(entry['recommended'])}")

def export_csv(data, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["package", "name", "category", "recommended"])
        writer.writeheader()
        writer.writerows(data)

def export_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def export_markdown(data, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("| Paketname | Kategorie | Name | Empfohlen |\n")
        f.write("|-----------|-----------|------|-----------|\n")
        for entry in data:
            f.write(f"| {entry['package']} | {entry['category']} | {entry['name']} | {entry['recommended']} |\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analysiert installierte Android-Pakete anhand lokaler Bloatware-Listen.")
    parser.add_argument("--csv", help="Exportiere als CSV-Datei", metavar="DATEINAME")
    parser.add_argument("--json", help="Exportiere als JSON-Datei", metavar="DATEINAME")
    parser.add_argument("--md", help="Exportiere als Markdown-Datei", metavar="DATEINAME")
    parser.add_argument("--lists", help="Pfad zum Verzeichnis mit den JSON-Listen", default="debloat_lists")
    args = parser.parse_args()

    db_dir = Path(args.lists)
    if not db_dir.exists():
        print(f"Verzeichnis '{db_dir}' nicht gefunden.")
        exit(1)

    installed = get_installed_packages()
    database = load_combined_bloatware_db(db_dir)
    classified = classify_packages(installed, database)

    print_table(classified)

    if args.csv:
        export_csv(classified, args.csv)
        print(f"CSV-Datei exportiert: {args.csv}")

    if args.json:
        export_json(classified, args.json)
        print(f"JSON-Datei exportiert: {args.json}")

    if args.md:
        export_markdown(classified, args.md)
        print(f"Markdown-Datei exportiert: {args.md}")
