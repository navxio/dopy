import subprocess


def main():
    subprocess.run(["twine", "upload", "dist/*"])
