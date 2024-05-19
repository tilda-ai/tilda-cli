import time
import subprocess
import threading
import pathspec

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def load_gitignore():
    """Load and parse the .gitignore file, returning a pathspec."""
    with open('.gitignore', 'r', encoding='utf-8') as file:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', file)
    return spec

class DebouncedBuilder(FileSystemEventHandler):
    """Handler that debounces build triggers, ignoring .gitignore files."""
    def __init__(self, cooldown=5):
        self.cooldown = cooldown
        self.gitignore_spec = load_gitignore()
        self.timer = None
        self.lock = threading.Lock()

    def should_ignore(self, path):
        """Check if the path should be ignored based on the .gitignore rules."""
        return self.gitignore_spec.match_file(path)

    def process_event(self):
        print("Building project...")
        subprocess.run(["python3", "-m", "build"])

    def on_any_event(self, event):
        if self.should_ignore(event.src_path) and 'src/lib' not in event.src_path:
            return

        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.cooldown, self.process_event)
            self.timer.start()

if __name__ == "__main__":
    WATCH_PATH = "./src"  # Path to watch
    event_handler = DebouncedBuilder()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    print(f"Watching {WATCH_PATH} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
