# list_packages.py

import subprocess

def list_android_packages():
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = [
            line.replace("package:", "").strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]
        return packages
    except subprocess.CalledProcessError as e:
        print("Fehler beim ADB-Aufruf:", e)
        return []

if __name__ == "__main__":
    print("📱 Installierte Android-Pakete:")
    packages = list_android_packages()
    for pkg in packages:
        print("  -", pkg)
    print(f"\nInsgesamt gefunden: {len(packages)} Pakete")
