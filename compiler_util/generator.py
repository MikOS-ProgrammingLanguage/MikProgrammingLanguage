import time, threading, os

from compiler_util.parser import RootNode
from compiler_util.preprocessor import *
from compiler_util.lexer import *
from compiler_util.parser import *
MIK = ["""

""", """

"""]
FINISHED = False
class Generator:
    def __init__(self, Root: RootNode, custom_types) -> None:
        self.root_node = Root
        self.is_n_main = False
        self.is_in_arg_parse = False
        self.custom_types = custom_types
        self.custom_types_arr = []
        for i in self.custom_types:
            self.custom_types_arr.append(i+"_arr")

    def generate(self):
        c_code = "int main(void) {"
		# can give linker errors lel
        is_n_main_code = "/*char* strcpy(char* dest, const char* src) {\ndo {*dest++ = *src++;}\nwhile (*src != 0);return 0;}*/\ntypedef unsigned long long uint64_t;\ntypedef unsigned int uint32_t;\ntypedef unsigned short uint16_t;\ntypedef unsigned char uint8_t;\ntypedef signed long long int64_t;\ntypedef signed int int32_t;\ntypedef signed short int16_t;\ntypedef signed char int8_t;\n//BUILTIN_END\n\n\n"
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
        if type(node) == AsignmentNode:
            if node.type_ == "int":
                code_ = self.__generate_int_asgn(node)
            elif node.type_ == "int_arr":
                code_ = self.__generate_int_arr_asgn(node)
            elif node.type_ == "str":
                code_ = self.__generate_str_asgn(node)
            elif node.type_ == "str_arr":
                code_ = self.__generate_str_arr_asgn(node)
            elif node.type_ == "flt":
                code_ = self.__generate_flt_asgn(node)
            elif node.type_ == "flt_arr":
                code_ = self.__generate_flt_arr_asgn(node)
            elif node.type_ == "char":
                code_ = self.__generate_char_asgn(node)
            elif node.type_ == "char_arr":
                code_ = self.__generate_char_arr_asgn(node)
            elif node.type_ == "cock":
                code_ = self.__generate_cock_asgn(node)
            elif node.type_ == "cock_arr":
                code_ = self.__generate_cock_arr_asgn(node)
            elif node.type_ in ("uint8", "uint16", "uint32", "uint64"):
                code_ = self.__generate_uint_asgn(node)
            elif node.type_.startswith("uint") and node.type_.endswith("_arr"):
                code_ = self.__generate_uint_arr_asgn(node)
            elif node.type_ in ("int8", "int16", "int32", "int64"):
                code_ = self.__generate_int_num_asgn(node)
            elif node.type_.startswith("int") and node.type_.endswith("_arr"):
                code_ = self.__generate_int_num_arr_asgn(node)
            elif node.type_ in self.custom_types:
                code_ = self.__generate_custom_type(node)
            elif node.type_ in self.custom_types_arr:
                code_ = self.__generate_custom_type_arr(node)
            else:
                NewError("well wtf")
            return code_, self.is_n_main
        elif type(node) == ReAsignementNode:
            if node.type_ == "int":
                code_ = self.__generate_int_reasgn(node)
            elif str(node.type_).startswith("int_arr_re"):
                code_ = self.__generate_int_arr_reasgn(node)
            elif node.type_ == "str":
                code_ = self.__generate_str_reasgn(node)
            elif node.type_.startswith("str_arr_re"):
                code_ = self.__generate_str_arr_reasgn(node)
            elif node.type_ == "flt":
                code_ = self.__generate_flt_reasgn(node)
            elif node.type_.startswith("flt_arr_re"):
                code_ = self.__generate_flt_arr_reasgn(node)
            elif node.type_ == "char":
                code_ = self.__generate_char_reasgn(node)
            elif (node.type_).startswith("char_arr_re"):
                code_ = self.__generate_char_arr_reasgn(node)
            elif node.type_ == "cock":
                code_ = self.__generate_cock_reasgn(node)
            elif (node.type_).startswith("cock_arr_re"):
                code_ = self.__generate_cock_arr_reasgn(node)
            elif node.type_ in ("uint8", "uint16", "uint32", "uint64"):
                code_ = self.__generate_uint_reasgn(node)
            elif node.type_ in ("int8", "int16", "int32", "int64"):
                code_ = self.__generate_int_num_reasgn(node)
            elif (node.type_).startswith("uint") and node.type_.endswith("_arr_re"):
                code_ = self.__generate_uint_arr_reasgn(node)
            elif (node.type_).startswith("int") and node.type_.endswith("_arr_re"):
                code_ = self.__generate_int_num_arr_reasgn(node)
            elif node.type_ in self.custom_types:
                code_ = self.__generate_custom_type_re(node)
            elif node.type_ in self.custom_types_arr:
                code_ = self.__generate_custom_type_re_arr(node)
            else:
                NewError("well wtf", node)
            return code_, self.is_n_main
        elif type(node) == BinOpNode:
            if ign_bin_op:
                NewError("OperationError", "You can't perform mathematical operations with type str!")
            code_ = self.__bin_op_node(node)
            return code_, self.is_n_main
        elif type(node) == IDNode:
            code_ = ""
            if node.deref:
                code_ += "&"
            code_ += str(node.tok)
            return code_, self.is_n_main
        elif type(node) == NumberNode:
            code_ = ""
            if node.deref:
                code_ += "&"
            code_ += str(node.tok.value)
            return code_, self.is_n_main
        elif type(node) == UnaryOpNode:
            code_ = ""
            if node.deref:
                code_ += "&"
            code_ += str(node.op_tok)+str(node.tok)
            return code_, self.is_n_main
        elif type(node) == StrNode:
            code_ = ""
            if node.deref:
                code_ += "&"
            code_ += "\""+str(node.tok.value)+"\""
            return code_, self.is_n_main
        elif type(node) == CharNode:
            code_ = ""
            if node.deref:
                code_ += "&"
            code_ += "'"
            code_ += str(node.tok.value)
            code_ += "'"
            return code_, self.is_n_main
        elif type(node) == ReturnNode:
            code_ = "return "+ str(self.__gen(node.tok)[0]) +";\n"
            return code_, self.is_in_arg_parse
        elif type(node) == StructNode:
            code_ = self.__generate_struct(node)
            return code_, True
        elif type(node) == EstructNode:
            code_ = self.__generate_struct(node, True)
            return code_, True
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
        elif type(node) == ElseNode:
            code_ = str(self.__generate_else(node))
            return code_, self.is_n_main
        elif type(node) == ElifNode:
            code_ = str(self.__generate_elif(node))
            return code_, self.is_n_main
        elif type(node) == WhileNode:
            code_ = str(self.__generate_while(node))
            return code_, self.is_n_main
        elif type(node) == ForNode:
            code_ = str(self.__generate_for(node))
            return code_, self.is_n_main
        elif type(node) == ArrayRefference:
            code_ = str(self.__generate_array_ref(node))
            return code_, self.is_n_main
        else:
            NewCritical("Ok you fucked with the compiler. STOP IT!")

    def __generate_array_ref(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.arr_len)[0])
        code_ += "]"
        return code_
    def __generate_custom_type(self, node):
        code = node.type_
        code += "* " if node.pointer else " "
        code += node.name
        if node.value != None:
            code += f" {node.op} "
            code += str(self.__gen(node.value)[0])
            code += ";\n" if not self.is_in_arg_parse else " "
            return code
        else:
            if self.is_in_arg_parse:
                code += ""
            else:
                code += ";\n"
            return code
    def __generate_custom_type_re(self, node):
        code_ = node.name
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
    def __generate_custom_type_arr(self, node):
        code = (node.type_).split("_arr")[0]
        code += "* " if node.pointer else " "
        code += node.name
        code += "["
        code += str(self.__gen(node.value)[0])
        code += "];\n"
        return code
    def __generate_custom_type_re_arr(self, node):
            code_ = node.name
            code_ += "["
            code_ += str(self.__gen(node.idx)[0])
            code_ += "] = "
            if node.value != None:
                code_ += str(self.__gen(node.value)[0])
                code_ += ";\n"
                return code_
            else:
                if self.is_in_arg_parse:
                    code_ += ""
                else:
                    code_ += ";\n"
                return code_

    def __generate_int_asgn(self, node):
        code_ = "int"
        code_ += "* " if node.pointer else " "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n" if not self.is_in_arg_parse else ""
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_int_arr_asgn(self, node):
        code_ = "int"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_
    def __generate_flt_asgn(self, node):
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
    def __generate_flt_arr_asgn(self, node):
        code_ = "float"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
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
    def __generate_str_arr_asgn(self, node):
        code_ = "char* "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_
    def __generate_char_asgn(self, node):
        #print("lol")
        code_ = "char"
        code_ += "* " if node.pointer else " "
        code_ += node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += ""
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += "';\n"
            return code_
    def __generate_char_arr_asgn(self, node):
        code_ = "char"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_
    def __generate_cock_asgn(self, node):
        code_ = "unsigned volatile long long int"
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
    def __generate_cock_arr_asgn(self, node):
        code_ = "unsigned volatile long long int"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_
    def __generate_uint_asgn(self, node):
        code_ = node.type_+"_t"
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
    def __generate_int_num_asgn(self, node):
        code_ = node.type_+"_t"
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
    def __generate_uint_arr_asgn(self, node):
        code_ = node.type_.split("_arr")[0]+"_t"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_
    def __generate_int_num_arr_asgn(self, node):
        code_ = node.type_.split("_arr")[0]+"_t"
        code_ += "* " if node.pointer else " "
        code_ += node.name+"["
        code_ += str(self.__gen(node.value)[0])
        code_ += "];\n"
        return code_

    def __generate_int_reasgn(self, node):
        code_ = node.name
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
    def __generate_int_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_flt_reasgn(self, node):
        code_ = node.name
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
    def __generate_flt_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_str_reasgn(self, node):
        code_ = "strcpy("
        code_ += node.name
        code_ += ","
        if node.value != None:
            code_ += str(self.__gen(node.value, True)[0])
            code_ += ");\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ""
            code_ += ");\n"
            return code_
    def __generate_str_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        code_ += f"strcpy({code_.split(' = ')[0]}, "
        if node.value != None:
            code_ += str(self.__gen(node.value, True)[0])
            code_ += ");\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ""
            code_ += ");\n"
        return code_
    def __generate_char_reasgn(self, node):
        #print("lol2")
        code_ = node.name
        if node.value != None:
            code_ += f" {node.op} "
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += "'"
            else:
                code_ += "';\n"
            return code_
    def __generate_char_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_cock_reasgn(self, node):
        code_ = node.name
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
    def __generate_cock_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_uint_reasgn(self, node):
        code_ = node.name
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
    def __generate_int_num_reasgn(self, node):
        code_ = node.name
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
    def __generate_uint_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
            code_ += ";\n"
            return code_
        else:
            if self.is_in_arg_parse:
                code_ += ""
            else:
                code_ += ";\n"
            return code_
    def __generate_int_num_arr_reasgn(self, node):
        code_ = node.name
        code_ += "["
        code_ += str(self.__gen(node.idx)[0])
        code_ += "] = "
        if node.value != None:
            code_ += str(self.__gen(node.value)[0])
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
        self.is_in_arg_parse = True
        for i in node.args:
            temp_args.append(str(self.__gen(i)[0]))
            temp_args.append(",")
        self.is_in_arg_parse = False
        del temp_args[len(temp_args)-1]
        for i in temp_args:
            f_call_str += i
        f_call_str += ");"
        return f_call_str


    def __generate_func(self, node):
        self.is_n_main = True
        self.is_in_arg_parse = True
        if node.ret_type == "str":
            node.ret_type = "char* "
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
        if node.func_decl:
            func_str += ");\n"
        else:
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
    def __generate_struct(self, node, e_struct=False):
        if node.typedef:
            code = f"typedef "
            if e_struct:
                code += "struct __attribute__((packed)) {\n"
            else:
                code += "struct {\n"
            for i in node.code_bl.code_bl_list:
                code += str(self.__gen(i)[0])
            code += "}"
            code += node.struct_name
            code += ";\n"
            return code
        else:
            if e_struct:
                code = "struct __attribute__((packed)) "
            else:
                code = "struct "
            code += node.struct_name
            code += "{\n"
            for i in node.code_bl.code_bl_list:
                code += str(self.__gen(i)[0])
            code += "};\n"
            return code

    def __generate_if(self, node):
        if_str = "if ("
        if_str += node.bool_bl.bool_statement
        if_str += ") {\n"
        for i in node.code_bl.code_bl_list:
            if_str += str(self.__gen(i)[0])
        if_str += "}\n"
        return if_str  
    def __generate_elif(self, node):
        elif_str = "else if ("
        elif_str += node.bool_bl.bool_statement
        elif_str += ") {\n"
        for i in node.code_bl.code_bl_list:
            elif_str += str(self.__gen(i)[0])
        elif_str += "}\n"
        return elif_str
    def __generate_else(self, node):
        else_str = "else {\n"
        for i in node.code_bl.code_bl_list:
            else_str += str(self.__gen(i)[0])
        else_str += "}\n"
        return else_str

    def __generate_while(self, node):
        while_str = "while ("
        while_str += node.bool_bl.bool_statement
        while_str += ") {\n"
        for i in node.code_bl.code_bl_list:
            while_str += str(self.__gen(i)[0])
        while_str += "}\n"
        return while_str
    def __generate_for(self, node):
        for_str = "for ("
        for_str += str(self.__gen(node.cnt_init)[0])
        for_str += node.bool_bl.bool_statement
        for_str += ";) {\n"
        for i in node.code_bl.code_bl_list:
            for_str += str(self.__gen(i)[0])
        for_str += "}\n"
        return for_str

    def __bin_op_node(self, node):
        left_c  = self.__gen(node.left_node)[0]
        op      = node.op_tok.value
        right_c = self.__gen(node.right_node)[0]
        return str(left_c)+str(op)+str(right_c)

    def __repr__(self) -> str:
        return "Why the fuck would you want to represent the code generator!"

#def __draw_mik():
#    idx = 0
#    while not FINISHED:
#        print(MIK[idx % len(MIK)], end="\r")
#        idx += 1
#        time.sleep(0.1)


def generate(args):
#    if args.mik:
#        # start thread with wayving mik
#        t1 = threading.Thread(target=__draw_mik)
#        t1.start()
    input_pth = args.i
    output_pth = args.o

    start = time.perf_counter()
    with open(input_pth, "r") as f:
        content = f.read()
        f.close()
    preprocessed = preprocess(content, input_pth)
    #print(preprocessed)
    lexed, sections = Lexer(preprocessed).lex()
    #print(lexed)
    if args.nCnfg == None:
        illegal_names = []
    else:
        illegal_names = args.nCnfg.split(":")
    parsed, c_types = Parser(lexed, illegal_names=illegal_names).parse()
    #print(parsed)
    #print(c_types)
    g = Generator(parsed, c_types).generate()
    with open(output_pth+".c", "w") as wf:
        wf.write(g)
        wf.close()
    #time.sleep(60)
    FINISHED = True
    end = time.perf_counter()
    NewInfo(f"File: {output_pth}.c successfully created in {end-start} seconds")
