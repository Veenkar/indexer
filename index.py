#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from pathlib import Path
import argparse


class Indexer:
    def __init__(self):
        pass

    def findFiles(self, extensions, searchdir=Path("."), rootdir=None, skip_paths=[]):
        searchdir = Path(searchdir)
        if rootdir == None:
            rootdir = searchdir

        rootdir = Path(rootdir)
        print(searchdir)

        if not isinstance(extensions, list):
            extensions = [extensions]

        paths = []
        for extension in extensions:
            # print(extension)
            searchexpr = "**/*{0}".format(extension)
            str_searchexpr = str(searchexpr)

            new_paths = searchdir.glob(str_searchexpr)
            new_paths = [path.relative_to(rootdir) for path in new_paths]
            new_paths = self.skipPaths(new_paths, skip_paths)
            if new_paths:
                paths += new_paths

        paths.sort()
        return paths


    def toGlob(self, paths):
        if isinstance(paths, list):
            return [Path(path) for path in paths]
        else:
            return Path(paths)


    def skipPaths(self, paths, skiplist):
        # paths = self.toGlob(paths)
        new_paths = []
        for path in paths:
            append = True
            for skip_path in skiplist:
                # TODO re-egzamine sh path matching (prev: if path.match(skip_path))
                if skip_path in str(path):
                    append = False
            if append:
                new_paths.append(str(path))
        return new_paths


    def fileLocations(self, files):
        dirs = []
        for file in files:
            basename = str(Path(file).parent)
            if not basename in dirs:
                # print(basename)
                dirs.append(basename)
        dirs.sort()
        return dirs


    def listToFile(self, in_list, filename):
        with open(filename, "w") as f:
            for item in in_list:
                f.write("%s\n" % item)


    def processProj( self,
        proj_name, proj_path, search_paths, skip_paths, include_extensions, other_extensions
    ):
        ## projdir
        projdir = Path(proj_path)
        projdir_abs = Path(projdir).absolute()
        proj_name = Path(proj_name).name

        print("PROJ NAME: {0}, PATH: {1}".format(proj_name, projdir_abs))


        include_files = []
        other_files = []
        for search_path in search_paths:
            include_files += self.findFiles(
                extensions=include_extensions,
                searchdir=projdir / search_path,
                rootdir=projdir,
                skip_paths=skip_paths,
            )
            other_files += self.findFiles(
                extensions=other_extensions,
                searchdir=projdir / search_path,
                rootdir=projdir,
                skip_paths=skip_paths,
            )

        files = include_files + other_files
        files.sort()

        include_dirs = self.fileLocations(include_files)

        self.listToFile(files, str(Path(proj_path) / "{0}.files".format(proj_name)))
        self.listToFile(include_dirs, str(Path(proj_path) / "{0}.includes".format(proj_name)))

        print(len(files))


# TEST
if __name__ == "__main__":
    ## options
    INCLUDE_EXTENSIONS = [".h", ".hpp", ".include"]
    OTHER_EXTENSIONS = [".c", ".cpp", ".cc", ".define", ".py"]
    SKIP_PATHS = ["cuda"]
    SEARCH_PATHS = ["tensorflow/core/kernels", "tensorflow/core/util"]
    DEFAULT_PROJS = ["tf"]

    ## options postprocess
    EXTENSIONS = INCLUDE_EXTENSIONS + OTHER_EXTENSIONS
    if not SEARCH_PATHS:
        SEARCH_PATHS = [""]


    parser = argparse.ArgumentParser(description="Indexer.")
    parser.add_argument("proj_name", nargs="*")
    args = parser.parse_args()

    print("Passed args: {0}".format(args.proj_name))

    if len(args.proj_name):
        projs = args.proj_name
    else:
        print("using default projs: {0}".format(DEFAULT_PROJS))
        projs = DEFAULT_PROJS

    ## rootdir
    rootdir = Path(".")
    rootdir_abs = Path(".").absolute()
    print("ROOT: {0}".format(rootdir_abs))

    indexer = Indexer()
    for proj_name in projs:
        indexer.processProj(
            proj_name,
            proj_name,
            SEARCH_PATHS,
            SKIP_PATHS,
            INCLUDE_EXTENSIONS,
            OTHER_EXTENSIONS,
        )
        # processProj(proj_name + "_updater", proj_name, SEARCH_PATHS, SKIP_PATHS, INCLUDE_EXTENSIONS, OTHER_EXTENSIONS)
