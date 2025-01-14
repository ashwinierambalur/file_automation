# IMPORTS
from os import scandir, rename
from os.path import splitext, exists, join
import shutil
import sys
import time
import logging
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

# File extensions, more can be added for video, audio, etc.
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
doc_extensions = [".pdf", ".doc", ".docx", ".txt"]

# Directories, add more if you want more variety of file extensions.
SOURCE_DIR = ""  # Your downloads directory (or other directory you want to watch for changes)
IMAGE_DIR = ""  # Where you want to place your images from your source
DOC_DIR = ""  # Where you want to place your documents from your source


def update_name(self, name, directory):  # Renames a file if one already exists in the dest directory
    count = 1
    file_name, file_extension = splitext(name)  # Ex. image.png -> filename = image, file_extension = .png
    logging.info(f"{file_name}{file_extension}")
    while exists(f"{directory}/{name}"):
        name = f"{file_name}{str(count)}{file_extension}"
        count += 1
    return name


def move_file(name, directory, download):
    if exists(f"{directory}/{name}"):  # Check if a file with the same name is in the dest directory
        old_name = f"{directory}/{name}"
        new_name = f"{directory}/{update_name(name, directory)}"
        rename(old_name, new_name)  # Renames the existing file in the directory
    move(download, directory)


class FileMovedHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            with scandir(SOURCE_DIR) as downloads:
                for download in downloads:
                    name = download.name
                    if self.check_images(name, download):
                        pass
                    if self.check_docs(name, download):
                        pass

    # If watching for another filetype, add directory above and add functions with a similar format as the others here.
    def check_images(self, name, download):
        for image_ext in image_extensions:
            if name.lower().endswith(image_ext):
                move_file(name, IMAGE_DIR, download)

    def check_docs(self, name, download):
        for doc_ext in doc_extensions:
            if name.lower().endswith(doc_ext):
                move_file(name, DOC_DIR, download)


# DO NOT TOUCH THE CODE BELOW
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = SOURCE_DIR
    event_handler = FileMovedHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
