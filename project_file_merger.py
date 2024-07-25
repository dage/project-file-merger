import os
import argparse
from typing import List, Set

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge project files and generate directory structure.")
    parser.add_argument("-d", "--directory", default=".", help="Project directory (default: current directory)")
    parser.add_argument("-o", "--output", default="project.txt", help="Output filename (default: project.txt)")
    parser.add_argument("-e", "--extensions", default=".py,.md,.env_template,.bat,.sh",
                        help="Comma-separated list of file extensions to include (default: .py,.md,.env_template,.bat,.sh)")
    parser.add_argument("-i", "--ignore_dirs", default=".git,.venv,venv,node_modules,__pycache__,build,dist",
                        help="Comma-separated list of directories to ignore (default: .git,.venv,venv,node_modules,__pycache__,build,dist)")
    return parser.parse_args()

def should_ignore(path: str, ignore_dirs: Set[str]) -> bool:
    return any(ignored in path.split(os.sep) for ignored in ignore_dirs)

def recursive_merge(directory: str, outfile, file_extensions: Set[str], ignore_dirs: Set[str]) -> int:
    file_count = 0
    root_dir = os.path.basename(os.path.abspath(directory))

    for root, dirs, files in os.walk(directory):
        if should_ignore(root, ignore_dirs):
            continue
        for file in files:
            if file.endswith(tuple(file_extensions)):
                file_path = os.path.join(root, file)
                relative_path = os.path.join(root_dir, os.path.relpath(file_path, directory))
                outfile.write(f"{'='*80}\n")
                outfile.write(f"File: {relative_path}\n")
                outfile.write(f"{'='*80}\n\n")
                try:
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                    outfile.write("\n\n")
                    file_count += 1
                except Exception as e:
                    outfile.write(f"ERROR: Unable to read file {relative_path}. Error: {str(e)}\n\n")
    return file_count

def generate_directory_listing(directory: str, ignore_dirs: Set[str]) -> List[str]:
    listing = []
    root_dir = os.path.basename(os.path.abspath(directory))
    for root, dirs, files in os.walk(directory):
        if should_ignore(root, ignore_dirs):
            continue
        level = root.replace(directory, '').count(os.sep)
        indent = '  ' * level
        listing.append(f"{indent}{os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for file in files:
            listing.append(f"{subindent}{file}")
    return [f"{root_dir}/"] + listing[1:]  # Prepend root directory to the listing

def main():
    args = parse_arguments()
    
    directory = os.path.abspath(args.directory)
    output_file = args.output
    file_extensions = set(args.extensions.split(','))
    ignore_dirs = set(args.ignore_dirs.split(','))

    # Generate directory listing
    directory_structure = generate_directory_listing(directory, ignore_dirs)

    # Write directory listing and merge files
    with open(output_file, 'w') as outfile:
        outfile.write("Project Directory Structure:\n")
        outfile.write("============================\n\n")
        outfile.write('\n'.join(directory_structure))
        outfile.write("\n\n")
        outfile.write("="*80 + "\n\n")
        outfile.write("Project Files Content:\n")
        outfile.write("======================\n\n")

        # Merge files
        file_count = recursive_merge(directory, outfile, file_extensions, ignore_dirs)

    print(f"Project merger completed:")
    print(f"- Directory processed: {directory}")
    print(f"- Output file: {output_file}")
    print(f"- File extensions included: {', '.join(file_extensions)}")
    print(f"- Directories ignored: {', '.join(ignore_dirs)}")
    print(f"- Total files processed: {file_count}")

if __name__ == "__main__":
    main()