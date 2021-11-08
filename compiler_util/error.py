from typing import NewType


class NewError:
    def __init__(self, err_type, description="", location="") -> None:
        self.err_t = err_type
        self.desc = description
        self.loc = location
        print(f"{self.err_t}! {self.desc} {self.loc}")
        quit()
