#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from pathlib import Path
import argparse

## options
INCLUDE_EXTENSIONS = [".h", ".hpp", ".include"]
OTHER_EXTENSIONS = [".c", ".cpp", ".cc", ".define"]
SKIP_PATHS = ["**/cuda/**"]
SEARCH_PATHS = ["tensorflow/core/kernels", "tensorflow/core/util"]
DEFAULT_PROJS=["tf"]

## options postprocess
EXTENSIONS = INCLUDE_EXTENSIONS + OTHER_EXTENSIONS
if not SEARCH_PATHS:
    SEARCH_PATHS = [""]

def findFiles(extensions, searchdir=Path("."), rootdir=None, skip_paths=[]):
    searchdir = Path(searchdir)
    if rootdir == None:
        rootdir = searchdir

    rootdir = Path(rootdir)
    print(searchdir)

    if not isinstance(extensions, list):
        extensions = [extensions]

    paths = []
    for extension in extensions:
        if not extension.startswith("."):
            extension = "." + extension
            pass

        #print(extension)
        searchexpr =  "**/*{0}".format(extension)
        str_searchexpr = str(searchexpr)

        new_paths = searchdir.glob(str_searchexpr)
        new_paths = [path.relative_to(rootdir) for path in new_paths]
        new_paths = skipPaths(new_paths, skip_paths)
        if new_paths:
            paths += new_paths

    paths.sort()
    return paths

def toGlob(paths):
    if isinstance(paths, list):
        return [Path(path) for path in paths]
    else:
        return Path(paths)

def skipPaths(paths, skiplist):
    #paths = toGlob(paths)
    new_paths = []
    for path in paths:
        append = True
        for skip_path in skiplist:
            if path.match(skip_path):
                append = False
        if append:
            new_paths.append(str(path))
    return new_paths

def fileLocations(files):
    dirs = []
    for file in files:
        basename = str(Path(file).parent)
        if not basename in dirs:
            #print(basename)
            dirs.append(basename)
    dirs.sort()
    return dirs

def listToFile(in_list, filename):
    with open(filename, 'w') as f:
        for item in in_list:
            f.write("%s\n" % item)


def processProj(proj_name):
    ## projdir
    projdir = Path(proj_name)
    proj_name_abs = Path(projdir).absolute()
    print("PROJ: {0}".format(proj_name_abs))

    include_files = []
    other_files = []
    for search_path in SEARCH_PATHS:
        include_files += findFiles(extensions=INCLUDE_EXTENSIONS, searchdir = projdir / search_path, rootdir = projdir, skip_paths=SKIP_PATHS)
        other_files += findFiles(extensions=OTHER_EXTENSIONS, searchdir = projdir / search_path, rootdir = projdir, skip_paths=SKIP_PATHS)

    files = ["index.py"] + include_files + other_files
    files.sort()

    include_dirs = fileLocations(include_files)

    listToFile(files, str(Path(proj_name) / "{0}.files".format(proj_name)) )
    listToFile(include_dirs, str(Path(proj_name) / "{0}.includes".format(proj_name)) )

    print(len(files))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Indexer.')
    parser.add_argument('proj_name', nargs="*")
    args = parser.parse_args()

    print("Passed args: {0}".format(args.proj_name))

    if len(args.proj_name):
        projs = args.proj_name
    else:
        print("using default projs: {0}".format(DEFAULT_PROJS))
        projs = DEFAULT_PROJS

    ## rootdir
    rootdir = Path(".")
    rootdir_abs=Path(".").absolute()
    print("ROOT: {0}".format(rootdir_abs))

    for proj_name in projs:
        processProj(proj_name)





