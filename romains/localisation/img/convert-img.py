# pip install watchdog pillow

import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

# Dossier à surveiller : dossier courant
WATCHED_FOLDER = os.getcwd()
SRC_FOLDER = os.path.join(WATCHED_FOLDER, "src")

# Créer le dossier "src" s'il n'existe pas
os.makedirs(SRC_FOLDER, exist_ok=True)

class PNGToJPGHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".png"):
            self.convert_and_move(event.src_path)

    def convert_and_move(self, png_path):
        try:
            # Attendre que le fichier soit complètement écrit
            time.sleep(1)

            with Image.open(png_path) as img:
                rgb_img = img.convert("RGB")
                jpg_path = os.path.splitext(png_path)[0] + ".jpg"
                rgb_img.save(jpg_path, "JPEG", quality=90)
                print(f"✅ Converti : {os.path.basename(png_path)} → {os.path.basename(jpg_path)}")

            # Déplacer l'original dans le dossier src/
            dest_path = os.path.join(SRC_FOLDER, os.path.basename(png_path))
            shutil.move(png_path, dest_path)
            print(f"📁 Déplacé dans : {dest_path}")

        except Exception as e:
            print(f"❌ Erreur lors de la conversion de {png_path} : {e}")

if __name__ == "__main__":
    print(f"📂 Surveillance du dossier courant : {WATCHED_FOLDER}")
    event_handler = PNGToJPGHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
