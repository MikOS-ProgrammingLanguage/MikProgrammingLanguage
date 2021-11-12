import time
from parser import RootNode
from preprocessor import *
from lexer import *
from parser import *

class Generator:
    def __init__(self, Root: RootNode) -> None:
        self.root_node = Root
        self.is_n_main = False
        self.is_in_arg_parse = False

    def generate(self):
        c_code = ""
        is_n_main_code = ""
        # iterate through all nodes and generate code for them
        for i in self.root_node.nodes:
            code = self.__gen(i)
            if code[1]:
                is_n_main_code += str(code[0])
            else:
                c_code += str(code[0])
        return is_n_main_code+c_code

    def __gen(self, node, ign_bin_op=False):
        code_ = None
        #print(type(node))
        if type(node) == AsignmentNode:
            if node.type_ == "int":
                code_ = self.__generate_int_asgn(node)
            elif node.type_ == "str":
                code_ = self.__generate_str_asgn(node)
            elif node.type_ == "flt":
                code_ = self.__generate_flt(node)
            elif node.type_ == "char":
                code_ = self.__generate_char(node)
            else:
                NewError("well wtf")
            return code_, self.is_n_main
        elif type(node) == BinOpNode:
            if ign_bin_op:
                NewError("OperationError", "You can't perform mathematical operations with type str or char!")
            code_ = self.__bin_op_node(node)
            return code_, self.is_n_main
        elif type(node) == IDNode:
            code_ = node.tok
            return code_, self.is_n_main
        elif type(node) == NumberNode:
            code_ = node.tok.value
            return code_, self.is_n_main
        elif type(node) == StrNode:
            code_ = node.tok.value
            return code_, self.is_n_main
        elif type(node) == CharNode:
            code_ = node.tok.value
            return code_, self.is_n_main
        elif type(node) == ReturnNode:
            code_ = "return "+node.tok.tok + ";\n"
            return code_, self.is_in_arg_parse
        elif type(node) == FunctionNode:
            code_ = self.__generate_func(node)
            return code_, True
        elif type(node) == FunctionCall:
            pass

    def __generate_int_asgn(self, node):
        code_ = "int"
        code_ += "* " if node.pointer else " "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_

    def __generate_flt(self, node):
        code_ = "float"
        code_ += "* " if node.pointer else " "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_

    def __generate_str_asgn(self, node):
        code_ = "char* "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value, True)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_

    def __generate_char(self, node):
        code_ = "char"
        code_ += "* " if node.pointer else " "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value, True)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_


    def __generate_func(self, node):
        self.is_n_main = True
        self.is_in_arg_parse = True
        func_str = f"{node.ret_type} {node.func_name} ("
        for i in node.arg_block.bool_bl_list:
            func_str += str(self.__gen(i)[0])
        self.is_in_arg_parse = False
        func_str += ") {"
        for b in node.code_block.code_bl_list:
            func_str += str(self.__gen(b)[0])
        func_str += "}\n"
        self.is_n_main = False
        return func_str


    def __bin_op_node(self, node):
        left_c  = self.__gen(node.left_node)[0]
        op      = node.op_tok.value
        right_c = self.__gen(node.right_node)[0]
        return str(left_c)+str(op)+str(right_c)

    def __repr__(self) -> str:
        return "Why the fuck would you want to represent the code generator!"

def generate(input_pth, output_pth):
    start = time.time()
    with open(input_pth[1], "r") as file:
        content = file.read()
    preprocessed = preprocess(content, input_pth[1])
    lexed, sections = Lexer(preprocessed).lex()
    parsed = Parser(lexed).parse()
    print(parsed)
    g = Generator(parsed).generate()
    print(g)
    end = time.time()
    print(end-start)
