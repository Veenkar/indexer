#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from index import *
import argparse
from pathlib import Path

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
