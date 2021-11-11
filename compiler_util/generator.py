import time
from parser import RootNode
from preprocessor import *
from lexer import *
from parser import *

class Generator:
    def __init__(self, Root: RootNode) -> None:
        self.root_node = Root
    
    def generate(self):
        c_code = ""
        # iterate through all nodes and generate code for them
        for i in self.root_node.nodes:
            c_code += self.__gen(i)
        return c_code

    def __gen(self, node, ign_bin_op=False):
        code_ = None
        if type(node) == AsignmentNode:
            if node.type_ == "int":
                code_ = self.__generate_int_asgn(node)
            elif node.type_ == "str":
                code_ = self.__generate_str_asgn(node)
            elif node.type_ == "flt":
                pass
            elif node.type_ == "char":
                pass
            else:
                NewError("well wtf")
            return code_
        elif type(node) == BinOpNode:
            if ign_bin_op:
                NewError("OperationError", "You can't perform mathematical operations with type str or char!")
            code_ = self.__bin_op_node(node)
            return code_
        elif type(node) == IDNode:
            code_ = node.tok
            return code_
        elif type(node) == NumberNode:
            code_ = node.tok.value
            return code_
        elif type(node) == StrNode:
            code_ = node.tok.value
            return code_
        elif type(node) == CharNode:
            code_ = node.tok.value
            return code_

    def __generate_int_asgn(self, node):
        code_ = "int "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value))
            code_ += ";\n"
            return code_
        else:
            code_ += ";\n"
            return code_

    def __generate_flt(self):
        pass

    def __generate_str_asgn(self, node):
        code_ = "char* "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value, True))
            code_ += ";\n"
            return code_
        else:
            code_ += ";\n"
            return code_

    def __generate_char(self):
        pass

    def __bin_op_node(self, node):
        left_c  = self.__gen(node.left_node)
        op      = node.op_tok.value
        right_c = self.__gen(node.right_node)
        return str(left_c+op+right_c)

    def __repr__(self) -> str:
        return "Why the fuck would you want to represent the code generator!"

def generate(input_pth, output_pth):
    start = time.time()
    with open(input_pth[1], "r") as file:
        content = file.read()
    preprocessed = preprocess(content, input_pth[1])
    lexed, sections = Lexer(preprocessed).lex()
    parsed = Parser(lexed).parse()
    g = Generator(parsed).generate()
    print(g)
    end = time.time()
    print(end-start)
