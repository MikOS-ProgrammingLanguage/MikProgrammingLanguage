# the Mik Package manager (mip)
from genericpath import isdir
import sys
import os
import shutil
from mip_util.pkg_parser import install_external, parse_pkg
from os import listdir
from os.path import isfile, join
import os.path
import time
from config import *

mip_src_path = src_path+"/mip-src/packages"
temp_src = src_path+"/mip-src/temp"

# Option execute
def list_pkgs():
    onlyfiles = [f for f in listdir(mip_src_path)]
    onlyfiles = sorted(onlyfiles, key=str.lower)
    print(f"You currently have {len(onlyfiles)} installed:\n")
    for i in onlyfiles:
        print(f"- {i}")

def remove(args: list):
    with open(src_path+"/mip-src/req_satisfied.txt", "r") as req_s_r:
        cntnts = req_s_r.read()
        req_s_r.close()
    new = ""
    for i in args:
        try:
            os.system(f"rmdir /Q /S \"{mip_src_path}/{i}\"")
            for y in cntnts.split("\n"):
                print(y)
                if y.endswith(i):
                    print("found pkg-src:::removing it")
                else:
                    new += y
            print(f"Succesfully removed {i}")
        except:
            print("Package not found!\n")
    with open(src_path+"/mip-src/req_satisfied.txt", "w") as req_s_w:
        req_s_w.write(new)
        req_s_w.close()

def install(args: list):
    if len(args) > 1:
        print("To many Arguments!\n")
    else:
        git_link = args[0]
        ret = install_external(git_link)
        if ret != None:
            add_pkg([ret])

def add_pkg(args: list):
    if len(args) > 1:
        print("To many Arguments!\n")
    else:
        f_path = args[0]
        if os.path.isdir(f_path):
            if os.path.isfile(f"{f_path}/milk.pkg"):
                # should parse and make a main.milk
                with open(f"{f_path}/milk.pkg", "r") as f:
                    content = f.read()
                    f.close()
                pkg_name, ignore = parse_pkg(content)
                current_wdir = f"{mip_src_path}/{pkg_name}"
                shutil.copytree(f_path, current_wdir)
                for i in ignore:
                    os.system(f"cd {current_wdir} && del {i}")
                        
                onlyfiles = [f for f in listdir(current_wdir) if isfile(join(current_wdir, f))]
                with open(current_wdir+"/main.milk", "w") as main_f:
                    for i in onlyfiles:
                        w_cntnt = f"#yoink <{i}>\n" if not i.endswith(".pkg") else ""
                        main_f.write(w_cntnt)
                print("\nSuccess!")
            else:
                print("No milk.pkg found at: "+f_path)
                print("Please make sure to add one!")
                quit()
        else:
            print("File not found: ", f_path)

# Handle
def handle_options(args: list):
    if not args:
        print("Help:\n")
        print("    - install -> installs a package via a github link ::: mip install <github-link>")
        print("    - add-pkg -> adds a package to your mip-src directory ::: mip add-pkg <relative-pkg-path>")
        print("    - remove -> removes specified packages by name ::: mip remove <pkg1> <pkg2> <...>")
        print("    - list -> lists all installed packages")
        print("    Wanna make your code public? Post it on github and make sure to include a 'milk.pk' file in the root dir")
    else:
        if args[0] == "install":
            install(args[1:])
        elif args[0] == "add-pkg":
            add_pkg(args[1:])
        elif args[0] == "remove":
            remove(args[1:])
        elif args[0] == "list":
            list_pkgs()
        else:
            print("Command not recognized")
if __name__=="__main__":
    del sys.argv[0]
    handle_options(sys.argv)
