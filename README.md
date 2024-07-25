# project-file-merger

A Python script that combines multiple project files into a single text file along with a recursive directory listing of the project file structure. Ideal for preparing codebases for LLM analysis or getting a comprehensive view of your project.

## Features

- Recursively scans directories
- Merges specified file types into one output file
- Creates a directory listing
- Skips specified directories
- Customizable via command-line options

## Usage

```bash
python project_file_merger.py [-h] [-d DIRECTORY] [-o OUTPUT] [-e EXTENSIONS] [-i IGNORE_DIRS]
```

### Arguments

The default arguments are picked based on the assumption the project is a Python project.

- `-d DIRECTORY, --directory DIRECTORY`: Project directory (default: current directory)
- `-o OUTPUT, --output OUTPUT`: Output filename (default: project.txt)
- `-e EXTENSIONS, --extensions EXTENSIONS`: Comma-separated list of file extensions (default: .py,.md,.env_template,.bat,.sh)
- `-i IGNORE_DIRS, --ignore_dirs IGNORE_DIRS`: Comma-separated list of directories to ignore (default: .git,.venv,venv,node_modules,__pycache__,build,dist)

### Example

```bash
python project_file_merger.py --directory /path/to/project --output merged_project.txt --extensions .py,.js,.css --ignore_dirs .git,node_modules,venv
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgment

This project was developed with significant assistance from Claude 3.5 Sonnet, an AI language model.