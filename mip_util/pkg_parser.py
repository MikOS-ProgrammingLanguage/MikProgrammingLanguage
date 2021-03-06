import os
import shutil
from os import listdir
from os.path import isfile, join
import os.path
from config import *
import compiler_util.error
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
                        w_cntnt = f"#yoink <{i}>\n" if not i.endswith(".pkg") else ""
                        main_f.write(w_cntnt)
                compiler_util.error.NewInfo("Success!")
                with open(f_path+"/main.milk", "r") as r_main_f:
                    code = r_main_f.read()
                    r_main_f.close()
                preprocessed = compiler_util.preprocessor.preprocess(code, f_path+"/main.milk", mip_pth=True)
                with open(f_path+"/main.milk", "w") as w_main_f:
                    w_main_f.write(preprocessed)
                    w_main_f.close()
            else:
                compiler_util.error.NewError(f"No milk.pkg was found at: {f_path}")
                compiler_util.error.NewInfo(f"Please make sure to add one!")
        else:
            compiler_util.error.NewCritical(f"File not found: {f_path}")

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
        compiler_util.error.NewWarning(f"requirement allready satisfied: {ext_name}", q=True)
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
                os.system(f"cd {current_wdir} && rm {i}")

            shutil.rmtree(temp_src)
            os.system(f"mkdir \"{temp_src}\"")
            with open(src_path+"/mip-src/req_satisfied.txt", "a") as ap:
                ap.write(f"{ext_name}:::{pkg_name2}\n")
            compiler_util.error.NewInfo(f"Successdully downloaded package: {pkg_name2}! You can now use it via: '#yoink-src <{pkg_name2}>'\n")
            add_pkg(mip_src_path+"/"+pkg_name2)
        else:
            compiler_util.error.NewError("No milk.pkg found at in Github repo! Please contact the developer")
            compiler_util.error.NewCritical("ABORTING", no_q=True)
            shutil.rmtree(temp_src)
            os.system(f"mkdir \"{temp_src}\"")

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
