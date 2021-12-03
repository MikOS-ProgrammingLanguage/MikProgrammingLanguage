import sys
import getopt
import argparse
from compiler_util.generator import *

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", required=True)
    parser.add_argument("-o", required=False, default="mik")
    parser.add_argument("--mik", required=False, action="store_true")
    parser.add_argument("-nCnfg")
    args = parser.parse_args()
    generate(args)
