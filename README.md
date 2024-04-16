
# ~tilda

~tilda is a command-line interface based on AI for managing system and development tasks. This tool is designed to simplify common administrative tasks and can be customized for specific workflows.

## Features

- **Manager Command**: Run tasks related to system management.
- **Terminal Command**: Execute specific commands directly in the terminal with optional permissive settings.

## Installation

To use the Tilda CLI Tool, you need Python installed on your system. The tool has been tested with Python 3.12.2. You can install it directly by cloning the repository and using it as a module.

\```bash
git clone https://github.com/tilda/tilda.git
cd tilda
uv venv
source .venv/bin/activate

\# build the package from source
python3 setup.py sdist bdist_wheel

\# exit venv
deactivate

\# install the tilda package on your machine
pipx install . --upgrade

tilda terminal "say hello"
\```

## Usage

After installation, the tool can be run from the command line. Here are some examples of how you can use the Tilda CLI Tool:

### Running the Terminal Agent

To run the terminal agent:

\```bash
tilda terminal "Say Hello, World!"
\```

To run the terminal command with permissive execution settings:

\```bash
terminal --careless "rm -rf /example"
\```

**Warning:** Use the `--careless` flag with caution, especially when performing operations that can modify or delete data.

## Contributing

Contributions to the Tilda CLI Tool are welcome! Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues if you find bugs or have feature requests.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
