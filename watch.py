import time
import subprocess
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DebouncedBuilder(FileSystemEventHandler):
    """Handler that debounces build triggers."""
    def __init__(self, cooldown=5):
        self.cooldown = cooldown
        self.last_scheduled = 0
        self.debounced_event = threading.Event()
        self.debounced_thread = threading.Thread(target=self.process_event)
        self.debounced_thread.start()

    def process_event(self):
        while True:
            self.debounced_event.wait()
            self.debounced_event.clear()
            time_now = time.time()
            if time_now - self.last_scheduled > self.cooldown:
                self.last_scheduled = time_now
                # Call the build command
                print("Building project...")
                subprocess.run(["python3", "-m", "build"])
                time.sleep(self.cooldown)

    def on_any_event(self, event):
        """Triggered on any file system event."""
        self.debounced_event.set()

if __name__ == "__main__":
    path = "./src"  # Path to watch
    event_handler = DebouncedBuilder()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching {path} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
