import os


def ls(path: str) -> str:
    files = []
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            print(f"The file {filename} is a directory")
            _files = ls(os.path.join(path, filename))
            files.extend(_files)
        elif os.path.isfile(os.path.join(path, filename)):
            files.append(os.path.join(path, filename))
        else:
            print(f"The file {filename} is not a file or directory")
    return files


files = ls(path=".")
for file in files:
    print(file)
