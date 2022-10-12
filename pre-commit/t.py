import os
import subprocess

from gitignore_parser import parse_gitignore
from pre_commit_hooks.end_of_file_fixer import main as end_of_file_main
from pre_commit_hooks.trailing_whitespace_fixer import main as trail_main

# get currend directory of where the script is called
cwd = os.getcwd()


if os.path.exists(f"{cwd}/.gitignore"):
    matches = parse_gitignore(f"{cwd}/.gitignore")
else:

    def matches(arg) -> bool:
        return False


def ls(path: str) -> list:
    files = []
    for filename in os.listdir(path):
        if matches(filename) or ".git" in filename:
            print(f"file {filename} matches gitignore, excluding")
            continue
        if os.path.isdir(os.path.join(path, filename)):
            _files = ls(os.path.join(path, filename))
            files.extend(_files)
        elif os.path.isfile(os.path.join(path, filename)):
            files.append(os.path.join(path, filename))
    return files


files = ls(path=cwd)

# run end of file fixer
end_of_file_main(files)

# run white space fixer
trail_main(files)

## Run tf fmt on the repo
tf_fmt = subprocess.Popen(
    ["terraform", "fmt", "-recursive", "-diff", cwd],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
stdout, stderr = tf_fmt.communicate(timeout=60)
if len(stdout) != 0:
    print(stdout)
