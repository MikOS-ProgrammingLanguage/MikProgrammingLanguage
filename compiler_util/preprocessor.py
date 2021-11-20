import os.path
import os
from config import *
# handles only relative paths
yoinked_files = []
yoinked_files_src = []

mip_src_path = src_path+"/mip-src/packages"
# handles yoink so no errors can appear if you yoink the same two times

PKG_PREPROCESS_FLAG = False
PKG_NAME = ""

def preprocess(text: str, start_file: str=None, start_f: bool=True, mip_pth=False) -> str:
    global PKG_PREPROCESS_FLAG, PKG_NAME
    new_text = ""

    if mip_pth:
        if start_file.endswith(".milk"):
            start_file = start_file.split("/")
            del start_file[len(start_file)-1]
            new = ""
            for i in start_file:
                new += i
                new += "/"
            start_file = new
        os.chdir(start_file)

    if start_f:
        start_file = start_file.replace("\\", "/")
        splt_f = start_file.split("/")
        w_dir = splt_f[0:(len(splt_f)-1)]
        new_w_str = ""
        for i in w_dir:
            new_w_str += i
            new_w_str += "/"
        if mip_pth:
            w_dir = os.getcwd()
        else:
            w_dir = os.getcwd()+"/"+new_w_str
        start_file = splt_f[len(splt_f)-1]
        new_text += f"@section(\"{start_file}\")\n"
    for i in text.split("\n"):
        if i.startswith("#yoink <") and i.endswith(">"):
            i2 = i.split("#yoink <")
            fname = (i2[1].split(">"))[0]
            if PKG_PREPROCESS_FLAG:
                fname = mip_src_path+"/"+PKG_NAME+"/"+fname
            if fname in yoinked_files:
                continue
            with open(w_dir+"/"+fname, "r")as file:
                new_text += f"@section(\"{fname}\")\n"
                content = file.read()
                content = content.split("\n")
                content2 = ""
                for i in content:
                    if (i.startswith("mikf") or i.startswith("const")) and i in text:
                        content2 += (i+" owt")
                    else:
                        content2 += i
                    content2 += "\n"
                new_content = preprocess(content2, start_f=False)
                yoinked_files.append(fname)
            new_text += new_content
        elif i.startswith("#yoink-src <") and i.endswith(">"):
            i2 = i.split("#yoink-src <")
            fname = (i2[1].split(">"))[0]
            if fname in yoinked_files_src:
                continue
            with open(mip_src_path+f"/{fname}/main.milk", "r")as file:
                new_text += f"@section(\"src_pkg->{fname}\")"
                content = file.read()
                content = content.split("\n")
                content2 = ""
                for i in content:
                    if (i.startswith("mikf") or i.startswith("const")) and i in text:
                        content2 += (i+" owt")
                    else:
                        content2 += i
                    content2 += "\n"
                PKG_PREPROCESS_FLAG = True
                PKG_NAME = fname
                new_content = preprocess(content2, start_f=False)
                PKG_PREPROCESS_FLAG = False
                PKG_NAME = ""
                yoinked_files_src.append(fname)
            new_text += new_content
        else:
            new_text += i
        new_text += "\n"
    new_text = new_text[0:len(new_text)-1]
    new_text += "@secend"
    return new_text
"""
TODO
    - import src
"""
