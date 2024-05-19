"""Get the tree structure of a directory."""
from pathlib import Path

from .get_project_root import get_project_root_path

from .is_file_in_git import is_file_in_git

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if not is_file_in_git(path) or path.name == '.git':
            continue
        yield prefix + pointer + path.name

        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)

def get_tree(dir_path: Path):
    """Get the tree structure of a directory."""
    return '\n'.join([line for line in tree(dir_path)])


def get_project_tree():
    """Get the tree structure of the project root directory."""
    return get_tree(get_project_root_path())