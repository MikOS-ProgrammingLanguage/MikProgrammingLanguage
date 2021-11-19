import os
import shutil
from os import listdir
from os.path import isfile, join
import os.path
from config import *
import compiler_util.preprocessor
MODULE_NAME = ""
EXTERNAL_PKGS = []
IGNORE_FILES = []

# is in config.py
mip_src_path = src_path+"/mip-src/packages"
temp_src = src_path+"/mip-src/temp"

def add_pkg(arg: str):
        def parse_pkg(text: str):
            IGNORE_FILES = []
            text = text.split("\n")
            for i in text:
                if i.startswith("module-name: "):
                    MODULE_NAME = i.split(" ")[1]
                elif i.startswith("external: "):
                    install_external(i.split(" ")[1])
                elif i.startswith("ignore-file: "):
                    IGNORE_FILES.append(i.split(" ")[1])
            return MODULE_NAME, IGNORE_FILES
        f_path = arg
        if os.path.isdir(f_path):
            if os.path.isfile(f"{f_path}/milk.pkg"):
                # should parse and make a main.milk
                onlyfiles = [f for f in listdir(f_path) if isfile(join(f_path, f))]
                with open(f_path+"/main.milk", "w") as main_f:
                    for i in onlyfiles:
                        w_cntnt = f"#yoink <{i}.milk>\n" if not i.endswith(".pkg") else ""
                        main_f.write(w_cntnt)
                print("\nSuccess!")
                with open(f_path+"/main.milk", "r") as r_main_f:
                    code = r_main_f.read()
                    r_main_f.close()
                preprocessed = compiler_util.preprocessor.preprocess(code, f_path+"/main.milk")
                print(preprocessed)
            else:
                print("No milk.pkg found at: "+f_path)
                print("Please make sure to add one!")
                quit()
        else:
            print("File not found: ", f_path)

def install_external(ext_name: str):    # clones a repo to a temporary folder and parses the pkg

    def parse_pkg2(text: str):
        IGNORE_FILES = []
        text = text.split("\n")
        for i in text:
            if i.startswith("module-name: "):
                MODULE_NAME = i.split(" ")[1]
            elif i.startswith("external: "):
                install_external(i.split(" ")[1])
            elif i.startswith("ignore-file: "):
                IGNORE_FILES.append(i.split(" ")[1])
        return MODULE_NAME, IGNORE_FILES
    with open(src_path+"/mip-src/req_satisfied.txt", "r") as req:
        req_satisfied = req.read()
        req.close()
    if ext_name in req_satisfied:
        print(f"\n-    requirement allready satisfied: {ext_name}")
    else:
        os.system(f"cd {temp_src} && cd .. && git clone {ext_name} temp")
        if os.path.isfile(f"{temp_src}/milk.pkg"):
            with open(f"{temp_src}/milk.pkg", "r") as f:
                content = f.read()
                f.close()
            pkg_name2, ignore2 = parse_pkg2(content)
            current_wdir = f"{mip_src_path}/{pkg_name2}"
            shutil.copytree(temp_src, current_wdir)
            for i in ignore2:
                os.system(f"cd {current_wdir} && del {i}")

            os.system(f"rmdir /Q /S \"{temp_src}\"")
            os.system(f"mkdir \"{temp_src}\"")
            with open(src_path+"/mip-src/req_satisfied.txt", "a") as ap:
                ap.write(f"{ext_name}:::{pkg_name2}\n")
            print(f"\nSucesfully downloaded package: {pkg_name2}! You can now use it via. '#yoink-src <{pkg_name2}>'\n")
            add_pkg(mip_src_path+"/"+pkg_name2)
        else:
            print("No milk.pkg found at in Github repo! Please contact the developer\nABORTING")
            os.system(f"rmdir /Q /S \"{temp_src}\"")
            os.system(f"mkdir \"{temp_src}\"")
            print("Aborted Successfully")

def parse_pkg(text: str):
    IGNORE_FILES = []
    text = text.split("\n")
    for i in text:
        if i.startswith("module-name: "):
            MODULE_NAME = i.split(" ")[1]
        elif i.startswith("external: "):
            install_external(i.split(" ")[1])
        elif i.startswith("ignore-file: "):
            IGNORE_FILES.append(i.split(" ")[1])
    return MODULE_NAME, IGNORE_FILES
