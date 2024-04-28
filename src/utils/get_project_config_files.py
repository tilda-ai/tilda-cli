import os
from pathlib import Path

from .get_file_project_path import get_file_project_path

def get_project_config_files():
    current_dir = Path.cwd()

    # Expanded list of potential project files with key identifiers for project types
    known_project_config_files = {
        'Node.js': ['package.json'],
        'Java (Maven)': ['pom.xml'],
        'Java (Gradle)': ['build.gradle'],
        'Python (setuptools)': ['setup.py'],
        'Python (pipenv)': ['Pipfile'],
        'Python (package)': ['pyproject.toml'],
        'C# (.NET)': ['.csproj', '.vbproj'],
        'Ruby': ['Gemfile'],
        'PHP (Composer)': ['composer.json'],
        'Rust': ['Cargo.toml'],
        'Go': ['go.mod'],
        'Elixir': ['mix.exs'],
        'Scala (sbt)': ['build.sbt'],
        'Frontend (web projects)': ['bower.json'],
        'Haskell': ['stack.yaml', 'cabal.config'],
        'R (R projects)': ['DESCRIPTION'],
        'Dart (Flutter)': ['pubspec.yaml'],
        'TypeScript': ['tsconfig.json'],
        'Swift (iOS/macOS)': ['Package.swift'],
        'Kotlin': ['build.gradle.kts'],
        'Clojure': ['project.clj'],
        'Erlang': ['rebar.config'],
        'Lua': ['Rockspec'],
        'Perl': ['Makefile.PL', 'Build.PL'],
        'Docker': ['Dockerfile'],
        'Ansible': ['ansible.cfg'],
        'Terraform': ['*.tf'],
        'Apache Ant': ['build.xml'],
        'ASP.NET': ['Web.config'],
        'Vue.js': ['vue.config.js'],
        'React Native': ['app.json'],
        'Angular': ['angular.json'],
        'Meteor': ['packages'],
        'Salesforce': ['sfdx-project.json']
    }

    markdown_languages = {
        'feature': 'Cucumber', 'abap': 'abap', 'ada': 'ada', 'ahk': 'ahk', 'apacheconf': 'apacheconf',
        'applescript': 'applescript', 'as': 'actionscript', 'asy': 'asy', 'bash': 'bash', 'bat': 'bat',
        'befunge': 'befunge', 'bmx': 'blitzmax', 'boo': 'boo', 'bf': 'brainfuck', 'c': 'c',
        'cfm': 'cfm', 'cheetah': 'cheetah', 'cl': 'common-lisp', 'clojure': 'clojure', 'cmake': 'cmake',
        'coffee': 'coffeescript', 'console': 'console', 'control': 'control', 'cpp': 'cpp', 'cs': 'csharp',
        'css': 'css', 'cython': 'cython', 'd': 'd', 'delphi': 'delphi', 'diff': 'diff',
        'dpatch': 'dpatch', 'duel': 'duel', 'dylan': 'dylan', 'erb': 'erb', 'erl': 'erl',
        'erlang': 'erlang', 'evoque': 'evoque', 'factor': 'factor', 'flx': 'felix', 'f': 'fortran',
        'gas': 'gas', 'genshi': 'genshi', 'glsl': 'glsl', 'gnuplot': 'gnuplot', 'go': 'go',
        'groff': 'groff', 'haml': 'haml', 'hs': 'haskell', 'html': 'html', 'hx': 'hx',
        'hy': 'hybris', 'ini': 'ini', 'io': 'io', 'ik': 'ioke', 'irc': 'irc',
        'jade': 'jade', 'java': 'java', 'js': 'javascript', 'jsp': 'jsp', 'lhs': 'lhs',
        'll': 'llvm', 'lgt': 'logtalk', 'lua': 'lua', 'mak': 'make', 'mao': 'mako',
        'maql': 'maql', 'mhtml': 'mason', 'md': 'markdown', 'mo': 'modelica', 'def': 'modula2',
        'moo': 'moocode', 'mu': 'mupad', 'mxml': 'mxml', 'myt': 'myghty', 'asm': 'nasm',
        'ns2': 'newspeak', 'objdump': 'objdump', 'm': 'objectivec', 'j': 'objectivej', 'ml': 'ocaml',
        'ooc': 'ooc', 'pl': 'perl', 'php': 'php', 'ps': 'postscript', 'pot': 'pot',
        'pov': 'pov', 'pro': 'prolog', 'properties': 'properties', 'proto': 'protobuf', 'py3tb': 'py3tb',
        'pytb': 'pytb', 'py': 'python', 'r': 'r', 'rb': 'rb', 'rconsole': 'rconsole',
        'rebol': 'rebol', 'redcode': 'redcode', 'rhtml': 'rhtml', 'rst': 'rst', 'sass': 'sass',
        'scala': 'scala', 'scaml': 'scaml', 'scm': 'scheme', 'scss': 'scss', 'st': 'smalltalk',
        'tpl': 'smarty', 'sources.list': 'sourceslist', 'sql': 'sql', 'sqlite3-console': 'sqlite3', 'squid.conf': 'squidconf',
        'ssp': 'ssp', 'tcl': 'tcl', 'tcsh': 'tcsh', 'tex': 'tex', 'txt': 'text',
        'v': 'v', 'vala': 'vala', 'vb': 'vbnet', 'vm': 'velocity', 'vim': 'vim',
        'xml': 'xml', 'xquery': 'xquery', 'xslt': 'xslt', 'yaml': 'yaml', 'toml': 'toml',
    }

    found_files = {}

    # Check each file in the list to see if it exists in the given path
    for project_type, filenames in known_project_config_files.items():
        for filename in filenames:
            file_path = os.path.join(current_dir, filename)
            if os.path.exists(file_path):
                # Extract file type (extension) or use filename if no extension
                _, ext = os.path.splitext(filename)
                file_type = ext[1:] if ext else filename  # remove the dot from the extension
                markdown_language = markdown_languages.get(file_type, 'text')

                with open(file_path, 'r', encoding="utf-8") as file:
                    content = file.read()
                    found_files[file_path] = {
                        'file_project_path': get_file_project_path(file_path),
                        'type': project_type,
                        'content': content,
                        'file_type': file_type,
                        'markdown_language': markdown_language
                    }

    if not found_files:
        return "No known project file found."

    return found_files
