#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from pathlib import Path
import argparse
import re

PRINT_PATHS=False

class Indexer:
    def __init__(self):
        self.all_paths = []
        pass

    def initDir(self, searchdir):

        searchdir = Path(searchdir)
        print(searchdir)
        self.all_paths = list(Path(searchdir).glob(str("**/*")))
        print("init dir: {0} {1}".format(searchdir, len(self.all_paths)))


    def findFilesFast(self, extensions, searchdir=Path("."), rootdir=None, skip_paths=[]):
        searchdir = Path(searchdir)

        if rootdir == None:
            rootdir = searchdir

        rootdir = Path(rootdir)

        if not isinstance(extensions, list):
            extensions = [extensions]

        paths = []
        for extension in extensions:
            # print(extension)
            searchexpr = ".*{0}$".format(re.escape(extension))
            regex = re.compile(searchexpr)

            #new_paths = filter(regex.match, self.all_paths)
            #new_paths = list(new_paths)

            new_paths = []
            for path in self.all_paths:
                if regex.match(str(path)):
                    new_paths += [path]

            new_paths = [path.relative_to(rootdir) for path in new_paths]
            new_paths = self.skipPaths(new_paths, skip_paths)
            if new_paths:
                paths += new_paths
            print("{0}: {1}".format(extension, len(new_paths)))
            if PRINT_PATHS:
                for path in new_paths:
                    print("\t{}".format(path))

        paths.sort()
        return paths

    def findFiles(self, extensions, searchdir=Path("."), rootdir=None, skip_paths=[]):
        searchdir = Path(searchdir)
        if rootdir == None:
            rootdir = searchdir

        rootdir = Path(rootdir)

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
            print("saving into: {}".format(filename))
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
            self.initDir(projdir / search_path)
            include_files += self.findFilesFast(
                extensions=include_extensions,
                searchdir=projdir / search_path,
                rootdir=projdir,
                skip_paths=skip_paths,
            )
            other_files += self.findFilesFast(
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
