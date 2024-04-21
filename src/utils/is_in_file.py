from fnmatch import fnmatch
import os


def is_in_file(filename, entry):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            content = file.read()
            if entry in content:
                return True
            else:
                # break the content into a list of lines
                content = content.split("\n")
                # check if the entry matches the line utilize shell-style wildcard matching
                for line in content:
                    if line:
                        if fnmatch(entry.strip('/'), line.strip('/')):
                            return True
                return False
    else:
        return False
