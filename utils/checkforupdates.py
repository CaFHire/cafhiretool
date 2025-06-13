import requests
import os
import time
import zipfile
import shutil
import hashlib
from bs4 import BeautifulSoup

MAIN_FILE_URL = "https://www.mediafire.com/file/69tvdo6ge3iis3m/main.py/file"
UTILS_ZIP_URL = "https://www.mediafire.com/file/abcd1234efgh567/utils.zip/file"  # Gerçek linki sen koy

TEMP_MAIN = "temp_main.py"
MAIN_FILE = "main.py"

TEMP_ZIP = "temp_utils.zip"
TEMP_DIR = "temp_utils"
UTILS_DIR = "utils"

def direct_download_url(mediafire_url):
    print("[*] Getting direct download link from MediaFire...")
    try:
        page = requests.get(mediafire_url).text
        soup = BeautifulSoup(page, "html.parser")
        button = soup.find("a", {"id": "downloadButton"})
        return button["href"]
    except Exception as e:
        print(f"[ERROR] Couldn't get download link: {e}")
        return None

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def hash_folder(path):
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        for name in sorted(files):
            with open(os.path.join(root, name), "rb") as f:
                while chunk := f.read(4096):
                    h.update(chunk)
    return h.hexdigest()

def update_main_py():
    print("\n[*] Checking main.py...")
    url = direct_download_url(MAIN_FILE_URL)
    if not url:
        return

    with open(TEMP_MAIN, "wb") as f:
        f.write(requests.get(url).content)

    if not os.path.exists(MAIN_FILE):
        print("[!] main.py not found. Saving new one.")
        os.rename(TEMP_MAIN, MAIN_FILE)
        print("[✓] main.py downloaded.")
        return

    local_hash = hash_file(MAIN_FILE)
    remote_hash = hash_file(TEMP_MAIN)

    if local_hash == remote_hash:
        print("[✓] main.py is already up to date.")
        os.remove(TEMP_MAIN)
    else:
        confirm = input("[!] main.py update available. Replace? (y/n): ").lower()
        if confirm == "y":
            os.replace(TEMP_MAIN, MAIN_FILE)
            print("[✓] main.py updated.")
        else:
            os.remove(TEMP_MAIN)
            print("[*] main.py update skipped.")

def update_utils():
    print("\n[*] Checking utils/ folder...")
    url = direct_download_url(UTILS_ZIP_URL)
    if not url:
        return

    with open(TEMP_ZIP, "wb") as f:
        f.write(requests.get(url).content)

    with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    if not os.path.exists(UTILS_DIR):
        print("[!] utils/ not found. Installing...")
        shutil.move(TEMP_DIR, UTILS_DIR)
        print("[✓] utils/ installed.")
        os.remove(TEMP_ZIP)
        return

    local_hash = hash_folder(UTILS_DIR)
    new_hash = hash_folder(TEMP_DIR)

    if local_hash == new_hash:
        print("[✓] utils/ is already up to date.")
        shutil.rmtree(TEMP_DIR)
    else:
        confirm = input("[!] utils/ update available. Replace? (y/n): ").lower()
        if confirm == "y":
            shutil.rmtree(UTILS_DIR)
            shutil.move(TEMP_DIR, UTILS_DIR)
            print("[✓] utils/ updated.")
        else:
            shutil.rmtree(TEMP_DIR)
            print("[*] utils/ update skipped.")

    os.remove(TEMP_ZIP)

def cleanup():
    if os.path.exists(TEMP_MAIN): os.remove(TEMP_MAIN)
    if os.path.exists(TEMP_ZIP): os.remove(TEMP_ZIP)
    if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR)

def check_for_all_updates():
    print("╔════════════════════════════════════╗")
    print("║     🔄 CAFO Tool Auto-Updater     ║")
    print("╚════════════════════════════════════╝")
    update_main_py()
    update_utils()
    cleanup()
    print("\n[✓] Update check complete.\n")

if __name__ == "__main__":
    check_for_all_updates()
