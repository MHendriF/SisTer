import os
import shutil
from os import path


def main():
    # make a duplicate of an existing file
    if path.exists("store/guru99.txt"):
        src = path.realpath("store/guru99.txt");

    # seperate the path from the filter
    head, tail = path.split(src)
    print("path:" + head)
    print("file:" + tail)

    # let's make a backup copy by appending "bak" to the name
    dst = src + ".bak"
    # nowuse the shell to make a copy of the file
    shutil.copy(src, dst)

    # copy over the permissions,modification
    shutil.copystat(src, dst)


if __name__ == "__main__":
    main()