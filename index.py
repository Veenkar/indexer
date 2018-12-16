#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from pathlib import Path

EXTENSIONS=[".h", ".hpp", ".include", ".c", ".cpp", ".cc", ".define"]

rootdir = Path(".")
rootdir_abs=Path(".").absolute()
print("ROOT: {0}".format(rootdir_abs))


def findFiles(extensions, searchdir="."):
    if not isinstance(extensions, list):
        extensions = [extensions]

    paths = []
    for extension in extensions:
        if not extension.startswith("."):
            extension = "." + extension
            pass

        print(extension)
        searchexpr = Path(searchdir) / "**" / "*{0}".format(extension)
        str_searchexpr = str(searchexpr)
        new_paths = glob.glob(str_searchexpr, recursive=True)
        if new_paths:
            paths += new_paths

    paths.sort()
    return paths

def listToFile(in_list, filename):
    with open(filename, 'w') as f:
        for item in in_list:
            f.write("%s\n" % item)

files = findFiles(EXTENSIONS)
files = ["indexer.py"] + files
listToFile(files, "indexer.files")


print(len(files))
