from pathlib import Path
from src.pkg.utils.get_project_root import get_project_root_path

def write_log_file(file_name, content):
    logs_dir = Path(get_project_root_path()) / '.tilda' / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    with open(logs_dir / file_name, 'w', encoding="utf-8") as file:
        file.write(content)
