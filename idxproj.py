#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from index import *
import argparse
from pathlib import Path
import argparse
import configparser
from pathlib import Path, PurePath


def main():
    cli_indexer = Cli_Indexer()
    cli_indexer.Perform_Indexing()

class Cli_Indexer:
    DEFAULT_INCLUDE_EXTENSIONS = [".h", ".hpp", ".include"]
    DEFAULT_OTHER_EXTENSIONS = [".c", ".cpp", ".cc", ".define", ".py", ".lua", ".txt"]

    def __init__(self):
        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument('config_path', type=PurePath,
                               help="path to the project .idx config file")
        self.args = self.argparser.parse_args()
        print(self.args)
        self.config_path = self.args.config_path
        self.Read_Config()

    @staticmethod
    def Read_Items(config_items):
        res = []
        for item in config_items:
            (key, val) = item
            #print(key)
            res.append(key)
        return res

    def Read_Config(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(str(self.config_path))

        print("CONFIG:")
        for section in self.config.sections():
            print("section {0}: ".format(section))
            print(self.config.items(section))
            print("")
        print("END CONFIG\n\n")

        try:
            self.name = self.config["general"]["name"]
            self.rootdir = self.config["general"]["rootdir"]
        except Exception as e:
            print(str(e))
            print("ERROR: did not find proper config in file {0}".format(self.config_path))

        self.search_paths = Cli_Indexer.Read_Items(self.config.items("search_paths"))
        self.skip_paths = Cli_Indexer.Read_Items(self.config.items("skip_paths"))

        try:
            self.include_extensions = Cli_Indexer.Read_Items(self.config.items("include_extensions"))
        except configparser.NoSectionError:
            self.include_extensions = self.DEFAULT_INCLUDE_EXTENSIONS

        try:
            self.other_extensions = Cli_Indexer.Read_Items(self.config.items("other_extensions"))
        except configparser.NoSectionError:
            self.other_extensions = self.DEFAULT_OTHER_EXTENSIONS

        print("search paths: {0}".format(self.search_paths))
        print("skip paths: {0}".format(self.skip_paths))


    def Perform_Indexing(self):
        ## options

        indexer = Indexer()
        indexer.processProj(
            self.name,
            self.rootdir,
            self.search_paths,
            self.skip_paths,
            self.include_extensions,
            self.other_extensions,
        )

if __name__ == "__main__":
    main()


# class cd:
#     """Context manager for changing the current working directory"""
#     def __init__(self, newPath):
#         self.newPath = os.path.expanduser(newPath)
#
#     def __enter__(self):
#         self.savedPath = os.getcwd()
#         os.chdir(self.newPath)
#
#     def __exit__(self, etype, value, traceback):
#         os.chdir(self.savedPath)
#


