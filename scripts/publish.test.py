import subprocess


def main():
    subprocess.run(["twine", "-r", "testpypi", "upload", "dist/*"])
