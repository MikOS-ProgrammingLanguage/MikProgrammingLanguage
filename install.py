import os

if __name__=="__main__":
    fpath = os.getcwd()
    fpath = fpath.replace("\\", "/")
    os.system("pip install colorama")
    with open("config.py", "w") as file:
        file.write(f"src_path = '{fpath}'")
        file.close()
    with open("compiler_util/config.py", "w") as file:
        file.write(f"src_path = '{fpath}'")
        file.close()
    with open("mip_util/config.py", "w") as file:
        file.write(f"src_path = '{fpath}'")
        file.close()
    print(f"Config has been updated succesfully to: '{fpath}'")
    input("PRESS ENTER")
