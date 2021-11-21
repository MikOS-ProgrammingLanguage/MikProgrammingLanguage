from typing import NewType
from colorama import Back, Fore, Style

class NewError:
    def __init__(self, err_type, description="", location="", no_q=False) -> None:
        self.err_t = err_type
        self.desc = description
        self.loc = location
        print(Fore.LIGHTRED_EX+f"[ERROR]: {self.err_t}! {self.desc} {self.loc}"+Fore.RESET)
        if not no_q:
            exit(-1)

class NewWarning:
    def __init__(self, warn_type, description="", location="", q=False) -> None:
        self.warn_type = warn_type
        self.descript = description
        self.loc = location
        print(Fore.MAGENTA+f"[WARNING]: {self.warn_type}! {self.descript} {self.loc}"+Fore.RESET)
        if q:
            exit(-1)

class NewCritical:
    def __init__(self, crit_type, description="", location="", no_q=False) -> None:
        self.crit_type = crit_type
        self.desc = description
        self.loc = location
        print(Fore.RED+f"[CRITICAL]: {self.crit_type}! {self.desc} {self.loc}"+Fore.RESET)
        if not no_q:
            exit(-1)

class NewInfo:
    def __init__(self, info: str, q=False) -> None:
        print(Fore.GREEN+f"[INFO]: {info}"+Fore.RESET)
        if q:
            exit(-1)
