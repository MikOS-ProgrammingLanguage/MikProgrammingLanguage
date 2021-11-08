import sys
import getopt
from compiler_util.generator import *

if __name__=="__main__":
    opts, args = getopt.getopt(sys.argv[1:], "i:o:")
    if not opts[1:]:
        print("No Opts specified!\n\n\t-i -> input\n\t-o -> output\n")
    else:
        generate(opts[0], opts[1])
