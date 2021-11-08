import os.path
from config import *
# handles only relative paths
yoinked_files = []
yoinked_files_src = []

mip_src_path = src_path+"/mip-src/packages"
# handles yoink so no errors can appear if you yoink the same two times

PKG_PREPROCESS_FLAG = False
PKG_NAME = ""

def preprocess(text: str) -> str:
    global PKG_PREPROCESS_FLAG, PKG_NAME
    new_text = ""
    for i in text.split("\n"):
        if i.startswith("#yoink <") and i.endswith(">"):
            i2 = i.split("#yoink <")
            fname = (i2[1].split(">"))[0]
            if PKG_PREPROCESS_FLAG:
                fname = mip_src_path+"/"+PKG_NAME+"/"+fname
            if fname in yoinked_files:
                continue
            with open(fname, "r")as file:
                content = file.read()
                content = content.split("\n")
                content2 = ""
                for i in content:
                    if (i.startswith("mikf") or i.startswith("mikcls") or i.startswith("const")) and i in text:
                        content2 += (i+" owt")
                    else:
                        content2 += i
                    content2 += "\n"
                new_content = preprocess(content2)
                yoinked_files.append(fname)
            new_text += new_content
        elif i.startswith("#yoink-src <") and i.endswith(">"):
            i2 = i.split("#yoink-src <")
            fname = (i2[1].split(">"))[0]
            if fname in yoinked_files_src:
                continue
            with open(mip_src_path+f"/{fname}/main.milk", "r")as file:
                content = file.read()
                content = content.split("\n")
                content2 = ""
                for i in content:
                    if (i.startswith("mikf") or i.startswith("mikcls") or i.startswith("const")) and i in text:
                        content2 += (i+" owt")
                    else:
                        content2 += i
                    content2 += "\n"
                PKG_PREPROCESS_FLAG = True
                PKG_NAME = fname
                new_content = preprocess(content2)
                PKG_PREPROCESS_FLAG = False
                PKG_NAME = ""
                yoinked_files_src.append(fname)
            new_text += new_content
        else:
            new_text += i
        new_text += "\n"

    return new_text
"""
TODO
    - import src
"""