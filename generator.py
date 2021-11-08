from parser import RootNode

class Generator:
    def __init__(self, Root: RootNode) -> None:
        self.root_node = Root
    
    def generate(self):
        pass

    def __generate_int(self):
        pass

    def __generate_flt(self):
        pass

    def __generate_str(self):
        pass

    def __generate_char(self):
        pass

    def __repr__(self) -> str:
        return "Why the fuck would you want to represent the code generator bro"