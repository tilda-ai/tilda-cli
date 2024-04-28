from pathlib import Path

from .get_project_root import get_project_root_path


def get_file_project_path(file_path: Path) -> Path:
    current_dir = Path.cwd()
    project_root = get_project_root_path()
    _file_path = Path(file_path)
    if _file_path.is_absolute():
        return _file_path.relative_to(project_root)
    else:
        return (current_dir / _file_path).resolve().relative_to(project_root)
    