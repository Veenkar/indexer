#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from pathlib import Path

INCLUDE_EXTENSIONS = [".h", ".hpp", ".include"]
OTHER_EXTENSIONS = [".c", ".cpp", ".cc", ".define"]

EXTENSIONS = INCLUDE_EXTENSIONS + OTHER_EXTENSIONS;

rootdir = Path(".")
rootdir_abs=Path(".").absolute()
print("ROOT: {0}".format(rootdir_abs))


def findFiles(extensions, searchdir=Path("."), skipdirs=[]):
    searchdir = Path(searchdir)

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

        new_paths_objs = [Path(strpath) for strpath in glob.glob(str_searchexpr, recursive=True)]

        new_paths = []
        for new_path_obj in new_paths_objs:
            append = True
            for skipdir in skipdirs:
                if new_path_obj.match(skipdir):
                    append = False
            if append:
                new_paths.append(str(new_path_obj))

        if new_paths:
            paths += new_paths

    paths.sort()
    return paths

def fileLocations(files):
    dirs = []
    for file in files:
        basename = str(Path(file).parent)
        if not basename in dirs:
            print(basename)
            dirs.append(basename)
    dirs.sort()
    return dirs

def listToFile(in_list, filename):
    with open(filename, 'w') as f:
        for item in in_list:
            f.write("%s\n" % item)

include_files = findFiles(INCLUDE_EXTENSIONS, skipdirs=["**/cuda/**"])
other_files = findFiles(OTHER_EXTENSIONS)

files = ["index.py"] + include_files + other_files
files.sort()

include_dirs = fileLocations(include_files)


listToFile(files, "indexer.files")
listToFile(include_dirs, "indexer.includes")

print(len(files))
