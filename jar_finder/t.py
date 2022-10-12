import zipfile
from pathlib import Path


def find_providers():
    for path in Path(".").rglob("*.jar"):
        print(f"File being analyzed: {path}")
        archive = zipfile.ZipFile(str(path), "r")
        for x in archive.namelist():
            if "BouncyCastleProvider.class" in x:
                print(f"Found BouncyCastleProvider.class in {x}")


def find_keystores():
    keystores = {"jks": [], "bcfks": []}
    keytypes = [".jks", ".bcfks"]

    for path in Path(".").rglob("*"):
        if path.is_file() and path.suffix in keytypes:
            keystores[path.suffix[1:]].append(str(path))

    return keystores


print(find_keystores())
