import time
from compiler_util.parser import RootNode
from compiler_util.preprocessor import *
from compiler_util.lexer import *
from compiler_util.parser import *

class Generator:
    def __init__(self, Root: RootNode) -> None:
        self.root_node = Root
        self.is_n_main = False
        self.is_in_arg_parse = False

    def generate(self):
        c_code = "int main(void) {"
        is_n_main_code = ""
        # iterate through all nodes and generate code for them
        for i in self.root_node.nodes:
            code = self.__gen(i)
            if code[1]:
                is_n_main_code += str(code[0])
            else:
                c_code += str(code[0])
        c_code += "}"
        return is_n_main_code + (c_code if len(c_code) != len("int main(void) {}") else "")

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
        elif type(node) == AssemblyNode:
            code_ = self.__generate_asm(node)
            return code_, True
        elif type(node) == FunctionCall:
            code_ = str(self.__generate_f_call(node))
            return code_, self.is_n_main
        elif type(node) == IfNode:
            code_ = str(self.__generate_if(node))
            return code_, self.is_n_main
        else:
            NewError("Ok you fucked with the compiler. STOP IT!")

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
            code_ += f" {node.op} \""
            code_ += str(self.__gen(node.value, True)[0])
            code_ += "\";\n"
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


    def __generate_f_call(self, node):
        f_call_str = f"{node.func_name}("
        temp_args = []
        for i in node.args:
            temp_args.append(str(self.__gen(i)[0]))
            temp_args.append(",")
        del temp_args[len(temp_args)-1]
        for i in temp_args:
            f_call_str += i
        f_call_str += ")"
        return f_call_str
        

    def __generate_func(self, node):
        self.is_n_main = True
        self.is_in_arg_parse = True
        func_str = f"{node.ret_type} {node.func_name} ("
        temp_args = []
        for i in node.arg_block.bool_bl_list:
            temp_args.append(str(self.__gen(i)[0]))
            temp_args.append(",")
        if temp_args != []:
            del temp_args[len(temp_args)-1]
        for i in temp_args:
            func_str += i
        self.is_in_arg_parse = False
        func_str += ") {\n"
        for b in node.code_block.code_bl_list:
            func_str += str(self.__gen(b)[0])
        func_str += "}\n"
        self.is_n_main = False
        return func_str
    def __generate_asm(self, node):
        self.is_n_main = True
        self.is_in_arg_parse = True
        asm_func_str = f"__attribute__((naked)) {node.ret_type} {node.func_name} ("
        temp_args = []
        for i in node.arg_block.bool_bl_list:
            temp_args.append(str(self.__gen(i)[0]))
            temp_args.append(",")
        if temp_args != []:
            del temp_args[len(temp_args)-1]
        for i in temp_args:
            asm_func_str += i
        self.is_in_arg_parse = False
        asm_func_str += ") { __asm__ __volatile__ (\""
        asm_func_str += node.code_block
        asm_func_str += "\");}\n"
        self.is_n_main = False
        return asm_func_str

    def __generate_if(self, node):
        if_str = "if ("
        if_str += node.bool_bl.bool_statement
        if_str += ") {\n"
        for i in node.code_bl.code_bl_list:
            if_str += str(self.__gen(i)[0])
        if_str += "}\n"
        return if_str

    def __bin_op_node(self, node):
        left_c  = self.__gen(node.left_node)[0]
        op      = node.op_tok.value
        right_c = self.__gen(node.right_node)[0]
        return str(left_c)+str(op)+str(right_c)

    def __repr__(self) -> str:
        return "Why the fuck would you want to represent the code generator!"

def generate(input_pth, output_pth):
    start = time.perf_counter()
    with open(input_pth[1], "r") as f:
        content = f.read()
        f.close()
    preprocessed = preprocess(content, input_pth[1])
    lexed, sections = Lexer(preprocessed).lex()
    #print(lexed)
    parsed = Parser(lexed).parse()
    g = Generator(parsed).generate()
    with open(output_pth[1]+".c", "w") as wf:
        wf.write(g)
        wf.close()
    end = time.perf_counter()
    NewInfo(f"File: {output_pth[1]}.c successfully created in {end-start} seconds")
