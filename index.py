#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
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


    def findFilesFast(self, extensions, searchdir=Path("."), rootdir=None, skip_paths=[], additional_searchexprs = None):
        searchdir = Path(searchdir)

        if rootdir == None:
            rootdir = searchdir

        rootdir = Path(rootdir)

        if not isinstance(extensions, list):
            extensions = [extensions]

        if additional_searchexprs is None:
            additional_searchexprs = []
        elif not isinstance(additional_searchexprs, list):
            additional_searchexprs = [additional_searchexprs]

        searchexprs = [".*{0}$".format(re.escape(extension)) for extension in extensions]
        searchexprs += additional_searchexprs

        paths = []
        for searchexpr in searchexprs:
            # print(extension)
            regex = re.compile(searchexpr, re.IGNORECASE)

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
            print("{0}:\t\t{1}".format(searchexpr, len(new_paths)))
            if PRINT_PATHS:
                for path in new_paths:
                    print("\t{}".format(path))

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
                if skip_path.lower() in str(path).lower():
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
        proj_name, proj_path, search_paths, skip_paths, include_extensions, other_extensions, additional_searchexprs=None
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
                additional_searchexprs=additional_searchexprs,
            )

        files = include_files + other_files
        files.sort()

        include_dirs = self.fileLocations(include_files)

        self.listToFile(files, str(Path(proj_path) / "{0}.files".format(proj_name)))
        self.listToFile(include_dirs, str(Path(proj_path) / "{0}.includes".format(proj_name)))

        print(len(files))

