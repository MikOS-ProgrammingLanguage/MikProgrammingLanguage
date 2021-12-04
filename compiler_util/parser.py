from compiler_util.preprocessor import *
from compiler_util.lexer import *
from compiler_util.error import *

CUSTOM_TYPES = {}
TYPES = [
    "int",
    "flt",
    "str",
    "char",
    "cock",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "int8",
    "int16",
    "int32",
    "int64"
]
INSTRUCTIONS = [
    "int",
    "flt",
    "str",
    "char",
    "mikf",
    "mikas",
    "struct",
    "estruct",
    "if",
    "else",
    "elif",
    "for",
    "while",
    "cock",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "int8",
    "int16",
    "int32",
    "int64"
]

# NODES

class RootNode:
    def __init__(self) -> None:
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def __repr__(self) -> str:
        return f"{self.nodes}"

class NumberNode:
    def __init__(self, tok) -> None:
        self.tok = tok
        self.deref = False

    def __repr__(self) -> str:
        return f"{self.tok}"

class StrNode:
    def __init__(self, tok) -> None:
        self.tok = tok
        self.deref = False

    def __repr__(self) -> str:
        return f"{self.tok}"

class CharNode:
    def __init__(self, tok) -> None:
        self.tok = tok
        self.deref = False
    
    def __repr__(self) -> str:
        return f"{self.tok}"

class TypeNode:
    def __init__(self, tok) -> None:
        self.tok = tok
        self.deref = False
    def __repr__(self) -> str:
        return f"{self.tok}"

class IDNode:
    def __init__(self, var_name, tok) -> None:
        self.tok = tok
        self.deref = False
    
    def __repr__(self) -> str:
        return f"{self.tok}"

class BoolNode:
    def __init__(self) -> None:
        self.bool_statement = ""
    
    def __repr__(self) -> str:
        return f"({self.bool_statement})"

class CodeBlock:
    def __init__(self) -> None:
        self.code_bl_list = []

    def add_arg(self, node):
        self.code_bl_list.append(node)
    
    def __repr__(self) -> str:
        return f"{self.code_bl_list}"

class IfNode:
    def __init__(self, bool_block:BoolNode, code_block: CodeBlock) -> None:
        self.bool_bl = bool_block
        self.code_bl = code_block
    
    def __repr__(self) -> str:
        return f"(if ({self.bool_bl})" + "{" + str(self.code_bl) + "})"

class ElseNode:
    def __init__(self, code_block: CodeBlock) -> None:
        self.code_bl = code_block
    def __repr__(self) -> str:
        return f"(else "+"{"+f"{self.code_bl}"+"})"

class ElifNode:
    def __init__(self, bool_block: BoolNode, code_block: CodeBlock) -> None:
        self.bool_bl = bool_block
        self.code_bl = code_block
    
    def __repr__(self) -> str:
        return f"(if ({self.bool_bl})"+ "{" + str(self.code_bl) + "})"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.right_node = right_node
        self.op_tok = op_tok
    
    def __repr__(self) -> str:
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, tok) -> None:
        self.op_tok = op_tok
        self.tok = tok
        self.deref = False
    
    def __repr__(self) -> str:
        return f"({self.op_tok}{self.tok})"

class AsignmentNode:
    def __init__(self, type_, pointer, name, op=None, value=None) -> None:
        self.type_ = type_
        self.pointer = pointer
        self.name = name
        self.value = value
        self.op = op
    
    def __repr__(self) -> str:
        return f"({self.type_} {self.name} {self.op} {self.value})"

class ReAsignementNode:
    def __init__(self, type_, pointer, name, op=None, value=None, arr=False) -> None:
        self.type_ = type_[0] if arr else type_
        self.pointer = pointer
        self.name = name
        self.value = value
        self.op = op
        if arr:
            self.idx = type_[1]
    
    def __repr__(self) -> str:
        return f"(re {self.type_} {self.name} {self.op} {self.value}"

class ArgBlockNode:
    def __init__(self) -> None:
        self.bool_bl_list = []
    def add_arg(self, node):
        self.bool_bl_list.append(node)
    
    def __repr__(self) -> str:
        return f"{self.bool_bl_list}"

class ArrayRefference:
    def __init__(self, name, arr_len) -> None:
        self.name = name
        self.arr_len = arr_len
    
    def __repr__(self) -> str:
        return f"(array: {self.name}[{self.arr_len}])"

class FunctionNode:
    def __init__(self, function_name, return_type, arg_block: ArgBlockNode, code_block: CodeBlock=CodeBlock(), func_decleration=False) -> None:
        self.func_name = function_name
        self.ret_type = return_type
        self.arg_block = arg_block
        self.code_block = code_block
        self.func_decl = func_decleration
    
    def __repr__(self) -> str:
        return f"({self.func_name} ({self.arg_block}) -> {self.ret_type} {self.code_block})"

class EstructNode:
    def __init__(self, struct_name, typedef, code_block) -> None:
        self.struct_name = struct_name
        self.typedef = typedef
        self.code_bl = code_block

class StructNode:
    def __init__(self, struct_name, typedef, code_block) -> None:
        self.struct_name = struct_name
        self.typedef = typedef
        self.code_bl = code_block
    
    def __repr__(self) -> str:
        return f"(struct {self.struct_name} {'typedef' if self.typedef else ''} "+"{"+str(self.code_bl)+"})"

class AssemblyNode:
    def __init__(self, function_name, return_type, arg_block: ArgBlockNode, asm) -> None:
        self.func_name = function_name
        self.ret_type = return_type
        self.arg_block = arg_block
        self.code_block = asm
    
    def __repr__(self) -> str:
        return f"({self.func_name} ({self.arg_block}) -> {self.ret_type} {self.code_block})"

class ReferenceNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    
    def __repr__(self) -> str:
        return f"{self.tok}"

class DebugNode:
    def __init__(self, debug_tok) -> None:
        self.debug_tok = debug_tok
    
    def __repr__(self) -> str:
        return f"(DEBUG-BREAKPOINT)"

class FunctionCall:
    def __init__(self, func_name, args) -> None:
        self.func_name = func_name
        self.args = args
    
    def __repr__(self) -> str:
        return f"({self.func_name} {self.args})"

class ReturnNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    def __repr__(self) -> str:
        return f"RETURN: {self.tok}"

class WhileNode:
    def __init__(self, bool_block:BoolNode, code_block:CodeBlock) -> None:
        self.bool_bl = bool_block
        self.code_bl = code_block
    def __repr__(self) -> str:
        return f"(if ({self.bool_bl}) "+"{"+str(self.code_bl)+"}"

class ForNode:
    def __init__(self, cnt_init, bool_block:BoolNode, code_block:CodeBlock) -> None:
        self.cnt_init = cnt_init
        self.bool_bl = bool_block
        self.code_bl = code_block
    def __repr__(self) -> str:
        return f"(for ({self.cnt_init}; {self.bool_bl}) " + "{" + str(self.code_bl) + "})"
# NODES END


class Parser:
    def __init__(self, tokens: list, illegal_names) -> None:
        self.__tokens = tokens
        self.__ilegal_names = illegal_names
        self.__pos = -1
        self.__current_token = None
        self.__programm_node = RootNode()
        self.__func_on = False
        self.VARS = {}
        self.FUNCTIONS = {}
        self.__advance()
    
    def __advance(self):
        self.__pos += 1
        if self.__pos < len(self.__tokens):
            self.__current_token = self.__tokens[self.__pos]
    
    def __get_token(self, num):
        pos_now = self.__pos
        return self.__tokens[pos_now+num] if pos_now+num < len(self.__tokens) else None

    def __check_and_make_type(self, node:CodeBlock):
        if self.__current_token.type_ in (TT_INT, TT_FLOAT):
            res = self.__expr() # gets tree for mathematical expr
            node.add_arg(res)
        elif self.__current_token.type_ == TT_ID:
            res = self.__mk_id()
            node.add_arg(res)
        elif self.__current_token.type_ == TT_KAND:
            res = self.__mk_id()
            try:
                res.deref = True
            except Exception as e:
                NewError("DerefferenceError", "You tried to derrefference something that can't be derefferenced")
            node.add_arg(res)
        elif self.__current_token.type_ == TT_DEBUG:
            node.add_arg(DebugNode(TT_DEBUG))
            self.__advance()
        elif self.__current_token.type_ == TT_OVERRIDE:
            self.__advance()
            prev_func = self.FUNCTIONS
            prev_vars = self.VARS
            self.VARS = {}
            self.FUNCTIONS = {}
            res = self.__mk_id()
            self.FUNCTIONS = prev_func
            self.VARS = prev_vars
        else:
            return node

        return node

    def parse(self):
        while self.__current_token.type_ != TT_EOF:
            if self.__current_token.type_ in (TT_INT, TT_FLOAT):
                res = self.__expr() # gets tree for mathematical expr
                self.__programm_node.add_node(res)
            elif self.__current_token.type_ == TT_ID:
                res = self.__mk_id()
                self.__programm_node.add_node(res)
            elif self.__current_token.type_ == TT_KAND:
                res = self.__mk_id()
                try:
                    res.deref = True
                except Exception as e:
                    NewError("DerefferenceError", "You tried to derrefference something that can't be derefferenced")
                self.__programm_node.add_node(res)
            elif self.__current_token.type_ == TT_DEBUG:
                self.__programm_node.add_node(DebugNode(TT_DEBUG))
                self.__advance()
            elif self.__current_token.type_ == TT_OVERRIDE:
                self.__advance()
                prev_func = self.FUNCTIONS
                prev_vars = self.VARS
                self.VARS = {}
                self.FUNCTIONS = {}
                res = self.__mk_id()
                self.FUNCTIONS = prev_func
                self.VARS = prev_vars
            else:
                break

        return self.__programm_node, CUSTOM_TYPES

    def __struct_get(self):
        if self.__get_token(1).type_ == TT_DOT and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
            temp_name = self.__current_token
            self.__advance()
            temp_name.value += "."
            self.__advance()
            temp_name.value += self.__current_token.value
            return temp_name
        elif self.__get_token(1).type_ == TT_ARROW and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
            temp_name = self.__current_token
            self.__advance()
            temp_name.value += "->"
            self.__advance()
            temp_name.value += self.__current_token.value
            return temp_name
        else:
            return self.__current_token

    def __factor(self):
        tok = self.__current_token
        if tok.type_ in (TT_INT, TT_FLOAT):
            self.__advance()
            return NumberNode(tok)
        elif tok.type_ == TT_MINUS:
            self.__advance()
            if self.__current_token.type_ == TT_MINUS:
                self.__advance()
                tok_ = self.__current_token
                self.__advance()
                return NumberNode(tok_)
            elif self.__current_token.type_ in (TT_INT, TT_FLOAT, TT_ID):
                if self.__current_token.type_ == TT_ID and self.__current_token.value in self.VARS and self.__get_token(1).type_ != TT_LBRK:
                    if self.__get_token(1).type_ == TT_DOT and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
                        temp_name = self.__current_token.value
                        self.__advance()
                        temp_name += "."
                        self.__advance()
                        temp_name += self.__current_token.value
                        return UnaryOpNode("-", temp_name)
                    elif self.__get_token(1).type_ == TT_ARROW and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
                        temp_name = self.__current_token.value
                        self.__advance()
                        temp_name += "->"
                        self.__advance()
                        temp_name += self.__current_token.value
                        return UnaryOpNode("-", temp_name)
                        
                    tok_ = self.__current_token
                    self.__advance()
                    return UnaryOpNode("-", tok_.value)
                else:
                    tok_ = self.__current_token
                    self.__advance()
                    return UnaryOpNode("-", tok_.value)
        elif tok.type_ in (TT_ID, TT_KAND):
            deref = False
            if tok.type_ == TT_KAND:
                deref = True
                self.__advance()
                tok = self.__struct_get()
                #tok = self.__current_token
            if tok.value in self.VARS and self.__get_token(1).type_ != TT_LBRK:
                tok2 = self.VARS.get(tok.value)
                tok2 = self.__struct_get()
                tok2 = tok2.value
            elif tok.value in self.VARS and self.__get_token(1).type_ == TT_LBRK:
                tok2 = self.VARS.get(tok.value)
                self.__advance()
                self.__advance()
                arr_len = self.__expr()
                self.__advance()
                return ArrayRefference(tok.value, arr_len)
            elif tok.value in self.FUNCTIONS:
                tok2 = self.FUNCTIONS.get(tok.value)
                tok2 = tok.value
            else:
                NewError("RefferencedBeforeAssignement", f"The variable '{tok.value}' is refferenced but not assigned!")
            self.__advance()
            node = IDNode(tok.value, tok2)
            node.deref = deref
            return node
        elif tok.type_ in (TT_STRING): 
            self.__advance()
            return StrNode(tok)
        elif tok.type_ in (TT_CHAR):
            self.__advance()
            return CharNode(tok)
    def __term(self):
        return self.__bin_op(self.__factor, (TT_MUL, TT_DIV))
    def __expr(self):
        return self.__bin_op(self.__term, (TT_PLUS, TT_MINUS))

    def __bin_op(self, func, ops):
        left = func()

        while self.__current_token.type_ in ops:
            op_tok = self.__current_token   # sets the op_tok bcs in while it must be mul/div
            self.__advance()
            right = func() # gets the right factor
            left = BinOpNode(left, op_tok, right)   # left factor is now bin op
        
        return left
    # needs types
    def __assign(self, type_, name_="", normal_decl=True):
        deref = False
        arr_len = ""
        self.__advance()
        if self.__current_token.type_ == TT_MUL:
            pointer = True
            self.__advance()
        else:
            pointer = False
        if self.__current_token.type_ == TT_ID:
            name = self.__current_token.value
            if name in self.VARS and self.__get_token(1).type_ != TT_REASGN:
                NewError("VariableNameDuplicate", f"The variable: {name} is already defined!", self.__current_token.ln_count)
            self.__advance()
            # should be = now
        elif name_ != "":
            name = name_
        if self.__current_token.type_ == TT_LBRK and not type_.endswith("_arr"):
            self.__advance()
            if self.__current_token.type_ == TT_RBRK:
                arr_len = ""
            else:
                arr_len = self.__expr()
                if self.__current_token.type_ != TT_RBRK:
                    NewError("Closing Bracket expected", f"at {self.__current_token.section} at line {self.__current_token.ln_count}")
                else:
                    self.__advance()
                    self.VARS.update({name:AsignmentNode(type_+"_arr", pointer, name, "=", arr_len)})
                    type_ += "_arr" if not type_.endswith("_arr") else ""
                    return AsignmentNode(type_, pointer, name, "=", arr_len)
        
        if self.__current_token.type_ in (TT_ASSGN, TT_REASGN) and normal_decl:
            asgn_op = "="
            self.__advance()
            if self.__current_token.type_ == TT_ID and self.__current_token.value in self.FUNCTIONS:
                f_name = self.__current_token.value
                value = self.FUNCTIONS.get(self.__current_token.value)
                len_args = len(value.arg_block.bool_bl_list)
                new_block = []
                self.__advance()
                if self.__current_token.type_ == TT_LPAREN:
                    self.__advance()
                    while self.__current_token.type_ != TT_RPAREN and self.__current_token.type_ != TT_EOF:
                        if self.__current_token.value == "int":
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value == "flt":
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value == "str":
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value == "char":
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value in CUSTOM_TYPES:
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value == "cock":
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value in ("uint8", "uint16", "uint32", "uint64"):
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value in ("int8", "int16", "int32", "int64"):
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.type_ == TT_COMMA:
                            self.__advance()
                            continue
                        else:
                            node = self.__mk_id()
                        new_block.append(node)
                    self.__advance()
                    #print(self.__current_token)
                    if len_args != len(new_block):
                        NewError("ParameterExpectedError", f"{len_args} args were expected but {len(new_block)} args were found!")
                    else:
                        self.VARS.update({name:AsignmentNode(type_, pointer, name, asgn_op, FunctionCall(f_name, new_block))})
                        return AsignmentNode(type_, pointer, name, asgn_op, FunctionCall(f_name, new_block))
            else:
                value = self.__expr()
                self.VARS.update({name:AsignmentNode(type_, pointer, name, asgn_op, value)})
                return AsignmentNode(type_, pointer, name, asgn_op, value)
        else:
            self.VARS.update({name:AsignmentNode(type_, pointer, name)})
            return AsignmentNode(type_, pointer, name)

    # needs types
    def __call_or_refference(self):
        call = self.__current_token
        call_name = self.__current_token.value
        old_c_name = call_name
        if self.__get_token(1).type_ == TT_DOT and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
            self.__advance()
            old_c_name = call_name + "."
            self.__advance()
            call_name = self.__current_token.value
            old_c_name += call_name
        elif self.__get_token(1).type_ == TT_ARROW and self.__get_token(2).type_ == TT_ID and (self.__get_token(2).value not in TYPES and self.__get_token(2).value not in INSTRUCTIONS and self.__get_token(2).value not in CUSTOM_TYPES):
            self.__advance()
            old_c_name = call_name + "->"
            self.__advance()
            call_name = self.__current_token.value
            old_c_name += call_name
        #print(self.VARS)

        if call.type_ in (TT_INT, TT_FLOAT, TT_STRING, TT_CHAR):
            node = self.__factor()
        elif call_name in self.VARS and call_name != "return":
            #print(self.__current_token)
            if self.VARS.get(call_name).type_.endswith("_arr"):
                prev_arr_len = self.VARS.get(call_name).value
                self.__advance()
                if self.__current_token.type_ == TT_LBRK:
                    self.__advance()
                    arr_len = self.__expr()
                    if self.__current_token.type_ == TT_RBRK:
                        if self.__get_token(1).type_ == TT_REASGN:
                            res = self.__assign(self.VARS.get(call_name).type_, name_=call_name)
                            self.VARS.update({call_name:AsignmentNode(res.type_, res.pointer, call_name, "=", prev_arr_len)})
                            new_res = ReAsignementNode((res.type_+"_re", arr_len), res.pointer, call_name, "=", res.value, True)
                            return new_res
                        elif self.__get_token(1).type_ == TT_ASSGN:
                            NewError("AssignedTwiceError", f"You tried to assign a value to an existing variable. Make sure to use '?=' at {self.__current_token.section} at line {self.__current_token.ln_count}")
                        else:
                            
                            NewError("CalledButNotAssignedError", f"Tried to call a Array at {self.__current_token.section} at line: {self.__current_token.ln_count}")
                    else:
                        NewError("BracketNotClosedError", f"Bracket was opened but never closed at: {self.__current_token.section} at line: {self.__current_token.ln_count}")
                else:
                    NewError("BracketExpectedError", f"A bracket was expected but not found at: {self.__current_token.section} at line: {self.__current_token.ln_count}")
            else:
                temp_node = self.__assign(type_=self.VARS.get(call_name).type_.lower(), name_=call_name)
                node = ReAsignementNode(temp_node.type_, temp_node.pointer, old_c_name, temp_node.op, temp_node.value)
        else:
            self.__advance()
            #print(self.__current_token)
            if self.__current_token.type_ == TT_LPAREN and call_name in self.FUNCTIONS:
                value = self.FUNCTIONS.get(call_name)
                len_args = len(value.arg_block.bool_bl_list)
                new_block = []
                self.__advance()
                while self.__current_token.type_ != TT_RPAREN and self.__current_token.type_ != TT_EOF:
                    if self.__current_token.value == "int":
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.value == "flt":
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.value == "str":
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.value == "char":
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.value in CUSTOM_TYPES:
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.type_ == TT_COMMA:
                        self.__advance()
                        continue
                    elif self.__current_token.value == "cock":
                        node2 = self.__assign(self.__current_token.value)
                    elif self.__current_token.valu in ("uint8", "uint16", "uint32", "uint64"):
                        node = self.__assign(self.__current_token.value)
                    elif self.__current_token.value in ("int8", "int16", "int32", "int64"):
                        node = self.__assign(self.__current_token.value)
                    else:
                        node2 = self.__mk_id()
                    new_block.append(node2)
                if len_args != len(new_block):
                    NewError("ParameterExpectedError", f"{len_args} args were expected but {len(new_block)} args were found!", f"-> Section {new_block[0].tok.section} at Line {new_block[0].tok.ln_count}")
                else:
                    node = FunctionCall(call_name, new_block)
                self.__advance()
            elif call.value == "return":
                node = ReturnNode(self.__factor())
            elif self.__current_token.type_ == TT_ID and self.__current_token.value in self.VARS:
                    #inf = self.VARS.get(self.__current_token.value)
                    #inf = inf.value
                    #node = ReferenceNode(inf)
                lol = self.__struct_get()
                node = IDNode(lol, lol)
            else:
                node = IDNode(old_c_name, old_c_name)
                #NewError("RefferenceError", self.__current_token)
        return node
    # needs types
    def __mikf(self):
        self.__advance()
        func_name = ""
        if self.__current_token.type_ == "ID" and self.__current_token.value not in self.VARS and self.__current_token.value not in self.FUNCTIONS and self.__current_token.value not in INSTRUCTIONS:
            func_name = self.__current_token.value
            ret_type = ""
            self.__advance()
            if self.__current_token.type_ == TT_LPAREN:
                old_vars = self.VARS
                self.VARS = {}
                self.__advance()
                bool_block_node = ArgBlockNode()
                while self.__current_token.type_ != TT_RPAREN:
                    tok = self.__current_token
                    next_tok = self.__get_token(2)
                    next_next_tok = self.__get_token(3)
                    if next_tok.type_ == TT_COMMA and next_next_tok.value not in (TYPES):
                        NewError("TypeExpectedError", f"A comma was found hence another type decleration was expected but not found! {self.__current_token}")
                    else:
                        if tok.value == "int":
                            node = self.__assign(tok.value)
                        elif tok.value == "flt":
                            node = self.__assign(tok.value)
                        elif tok.value == "str":
                            node = self.__assign(tok.value)
                        elif tok.value == "char":
                            node = self.__assign(tok.value)
                        elif tok.type_ == "COMMA":
                            self.__advance()
                            continue
                        elif tok.value == "cock":
                            node = self.__assign(tok.value)
                        elif tok.value in TYPES and tok.value not in ("int", "flt", "str", "char", "cock"):
                            node = self.__assign(tok.value)
                        elif self.__current_token.valu in ("uint8", "uint16", "uint32", "uint64"):
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value in ("int8", "int16", "int32", "int64"):
                            node = self.__assign(self.__current_token.value)
                        else:
                            NewError("InvalidTypeError", f"You specified an invalid type in function decleration: {self.__current_token}")
                        bool_block_node.add_arg(node)
                self.__advance()
                if self.__current_token.type_ == TT_ARROW:
                    self.__advance()
                    if self.__current_token.value in TYPES:
                        ret_type = self.__current_token.value
                        if ret_type in ("uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32", "int64"):
                            ret_type += "_t"
                        self.__advance()
                        if self.__current_token.type_ == TT_MUL:
                            ret_type += "* "
                            self.__advance()
                    else:
                        NewError("NoReturnTypeFoundError", "There was a return type expected but not found")
                else:
                    ret_type = "void"
                if self.__current_token.type_ == TT_LCURL:
                    self.__func_on = True
                    code_block = CodeBlock()
                    self.__advance()
                    while self.__current_token.type_ != TT_RCURL:
                        code_block = self.__check_and_make_type(code_block)
                    self.__advance()
                    self.__func_on = False
                    func_decl = False
                else:
                    code_block = CodeBlock()
                    func_decl = True
            self.VARS = old_vars
            if func_name in self.__ilegal_names and not func_decl:
                NewError("Function is allready defined in another file.")
            else:
                self.FUNCTIONS.update({f"{func_name}":FunctionNode(func_name, ret_type, bool_block_node, code_block, func_decl)})
                return FunctionNode(func_name, ret_type, bool_block_node, code_block, func_decl)
        else:
            NewError("Function is allready defined")
    # needs types
    def __mikas(self):
        self.__advance()
        func_name = ""
        if self.__current_token.type_ == "ID" and self.__current_token.value not in self.VARS and self.__current_token.value not in self.FUNCTIONS and self.__current_token.value not in INSTRUCTIONS:
            func_name = self.__current_token.value
            ret_type = ""
            self.__advance()
            if self.__current_token.type_ == TT_LPAREN:
                old_vars = self.VARS
                self.VARS = {}
                self.__advance()
                bool_block_node = ArgBlockNode()
                while self.__current_token.type_ != TT_RPAREN:
                    tok = self.__current_token
                    next_tok = self.__get_token(2)
                    next_next_tok = self.__get_token(3)
                    if next_tok.type_ == TT_COMMA and next_next_tok.value not in (TYPES):
                        NewError("TypeExpectedError", f"A comma was found hence another type decleration was expected but not found! {self.__current_token}")
                    else:
                        if tok.value == "int":
                            node = self.__assign(tok.value)
                        elif tok.value == "flt":
                            node = self.__assign(tok.value)
                        elif tok.value == "str":
                            node = self.__assign(tok.value)
                        elif tok.value == "char":
                            node = self.__assign(tok.value)
                        elif tok.type_ == "COMMA":
                            self.__advance()
                            continue
                        elif tok.value == "cock":
                            node = self.__assign(tok.value)
                        elif tok.value in TYPES and tok.value not in ("int", "flt", "str", "char", "cock"):
                            node = self.__assign(tok.value)
                        elif self.__current_token.valu in ("uint8", "uint16", "uint32", "uint64"):
                            node = self.__assign(self.__current_token.value)
                        elif self.__current_token.value in ("int8", "int16", "int32", "int64"):
                            node = self.__assign(self.__current_token.value)
                        else:
                            NewError("InvalidTypeError", f"You specified an invalid type in function decleration: {self.__current_token}")
                        bool_block_node.add_arg(node)
                self.__advance()
                if self.__current_token.type_ == TT_ARROW:
                    self.__advance()
                    if self.__current_token.value in TYPES:
                        ret_type = self.__current_token.value
                        if ret_type in ("uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32", "int64"):
                            ret_type += "_t"
                        self.__advance()
                        if self.__current_token.type_ == TT_MUL:
                            ret_type += "* "
                            self.__advance()
                    else:
                        NewError("NoReturnTypeFoundError", "There was a return type expected but not found")
                else:
                    ret_type = "void"
                if self.__current_token.type_ == TT_LCURL:
                    self.__func_on = True
                    self.__advance()
                    asm_code = self.__current_token.value
                    self.__advance()
                    self.__func_on = False
                else:
                    NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            self.VARS = old_vars
            self.FUNCTIONS.update({f"{func_name}":FunctionNode(func_name, ret_type, bool_block_node, asm_code)})
            return AssemblyNode(func_name, ret_type, bool_block_node, asm_code)
    # needs types
    def __struct(self, e_struct=False):
        typedef = False
        name = ""
        self.__advance()
        if self.__current_token.type_ == TT_ID:
            name = self.__current_token.value
            self.__advance()
            if self.__current_token.type_ == TT_ID and self.__current_token.value == "typedef":
                typedef = True
                self.__advance()
            if self.__current_token.type_ == TT_LCURL:
                self.__advance()
                code_block = CodeBlock()
                names = []
                while self.__current_token.type_ != TT_RCURL and self.__current_token != None:
                    tok = self.__current_token
                    if tok.value == "int":
                        node = self.__assign(tok.value)
                    elif tok.value == "flt":
                        node = self.__assign(tok.value)
                    elif tok.value == "str":
                        node = self.__assign(tok.value)
                    elif tok.value == "char":
                        node = self.__assign(tok.value)
                    elif tok.value == "cock":
                        node = self.__assign(tok.value)
                    elif tok.value in TYPES and tok.value not in ("int", "flt", "str", "char", "cock"):
                        node = self.__assign(tok.value)
                    elif self.__current_token.valu in ("uint8", "uint16", "uint32", "uint64"):
                        node = self.__assign(self.__current_token.value)
                    elif self.__current_token.value in ("int8", "int16", "int32", "int64"):
                        node = self.__assign(self.__current_token.value)
                    else:
                        NewError("IllegalDeclarationError", f"Illegal decleration in struct at {self.__current_token.section} at line {self.__current_token.ln_count}")
                    code_block.add_arg(node)
                    names.append(node.name)
                self.__advance()
                if typedef:
                    TYPES.append(name)
                    CUSTOM_TYPES.update({name:names})
                if e_struct:
                    return EstructNode(name, typedef, code_block)
                else:
                    return StructNode(name, typedef, code_block)
            else:
                NewError("CurlyBracketExpectedError", f"A curly bracket was expected but not found at {self.__current_token.section} at line {self.__current_token.ln_count}")
        else:
            NewError("FunctionNameExpectedError", f"A struct name was expected but not found at {self.__current_token.section} at line {self.__current_token.ln_count}")

    def __if(self):
        self.__advance()
        if self.__current_token.type_ == TT_LPAREN:
            bool_block = BoolNode()
            self.__advance()
            while self.__current_token != None:
                tok = self.__current_token
                if tok.type_ in (TT_INT, TT_FLOAT):
                    bool_block.bool_statement += str(tok.value)
                    self.__advance()
                elif tok.type_ == TT_STRING:
                    bool_block.bool_statement += f"\"{tok.value}\""
                    self.__advance()
                elif tok.type_ == TT_CHAR:
                    bool_block.bool_statement += f"'{tok.value}'"
                    self.__advance()
                elif tok.type_ == TT_ID and tok.value in self.VARS:
                    bool_block.bool_statement += str(self.__expr())
                elif tok.type_ == TT_KAND:
                    bool_block.bool_statement += "&"
                    self.__advance()
                elif tok.type_ == TT_NOT:
                    bool_block.bool_statement += " !"
                    self.__advance()
                elif tok.type_ == TT_EQ:
                    bool_block.bool_statement += " == "
                    self.__advance()
                elif tok.type_ == TT_NEQ:
                    bool_block.bool_statement += " != "
                    self.__advance()
                elif tok.type_ == TT_LTHEN:
                    bool_block.bool_statement += " < "
                    self.__advance()
                elif tok.type_ == TT_GTHEN:
                    bool_block.bool_statement += " > "
                    self.__advance()
                elif tok.type_ == TT_LEQ:
                    bool_block.bool_statement += " <= "
                    self.__advance()
                elif tok.type_ == TT_GEQ:
                    bool_block.bool_statement += " >= "
                    self.__advance()
                elif tok.type_ == TT_AND:
                    bool_block.bool_statement += " && "
                    self.__advance()
                elif tok.type_ == TT_OR:
                    bool_block.bool_statement += " || "
                    self.__advance()
                elif tok.type_ == TT_RPAREN:
                    self.__advance()
                    break
                else:
                    NewError("IllegalBoolStatement", "An illegal bool statement was found: ", tok)
            
            if self.__current_token.type_ == TT_LCURL:
                code_block = CodeBlock()
                self.__advance()
                while self.__current_token.type_ != TT_RCURL:
                    code_block = self.__check_and_make_type(code_block)
                self.__advance()
            else:
                NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            return IfNode(bool_block, code_block)
    def __else(self):
        self.__advance()
        if self.__current_token.type_ == TT_LCURL:
            code_block = CodeBlock()
            self.__advance()
            while self.__current_token.type_ != TT_RCURL:
                code_block = self.__check_and_make_type(code_block)
            self.__advance()
        else:
            NewError("NoCodeBlockError", "No code block '{}' was started but one was expected")
        return ElseNode(code_block)
    def __elif(self):
        self.__advance()
        if self.__current_token.type_ == TT_LPAREN:
            bool_block = BoolNode()
            self.__advance()
            while self.__current_token != None:
                tok = self.__current_token
                if tok.type_ in (TT_INT, TT_FLOAT):
                    bool_block.bool_statement += str(tok.value)
                    self.__advance()
                elif tok.type_ == TT_STRING:
                    bool_block.bool_statement += f"\"{tok.value}\""
                    self.__advance()
                elif tok.type_ == TT_CHAR:
                    bool_block.bool_statement += f"'{tok.value}'"
                    self.__advance()
                elif tok.type_ == TT_ID and tok.value in self.VARS:
                    bool_block.bool_statement += str(self.__expr())
                elif tok.type_ == TT_KAND:
                    bool_block.bool_statement += "&"
                    self.__advance()
                elif tok.type_ == TT_NOT:
                    bool_block.bool_statement += " !"
                    self.__advance()
                elif tok.type_ == TT_EQ:
                    bool_block.bool_statement += " == "
                    self.__advance()
                elif tok.type_ == TT_NEQ:
                    bool_block.bool_statement += " != "
                    self.__advance()
                elif tok.type_ == TT_LTHEN:
                    bool_block.bool_statement += " < "
                    self.__advance()
                elif tok.type_ == TT_GTHEN:
                    bool_block.bool_statement += " > "
                    self.__advance()
                elif tok.type_ == TT_LEQ:
                    bool_block.bool_statement += " <= "
                    self.__advance()
                elif tok.type_ == TT_GEQ:
                    bool_block.bool_statement += " >= "
                    self.__advance()
                elif tok.type_ == TT_AND:
                    bool_block.bool_statement += " && "
                    self.__advance()
                elif tok.type_ == TT_OR:
                    bool_block.bool_statement += " || "
                    self.__advance()
                elif tok.type_ == TT_RPAREN:
                    self.__advance()
                    break
                else:
                    NewError("IllegalBoolStatement", "An illegal bool statement was found: ", tok)
            
            if self.__current_token.type_ == TT_LCURL:
                code_block = CodeBlock()
                self.__advance()
                while self.__current_token.type_ != TT_RCURL:
                    code_block = self.__check_and_make_type(code_block)
                self.__advance()
            else:
                NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            return ElifNode(bool_block, code_block)

    def __while(self):
        self.__advance()
        if self.__current_token.type_ == TT_LPAREN:
            bool_block = BoolNode()
            self.__advance()
            while self.__current_token != None:
                tok = self.__current_token
                if tok.type_ in (TT_INT, TT_FLOAT):
                    bool_block.bool_statement += str(tok.value)
                    self.__advance()
                elif tok.type_ == TT_STRING:
                    bool_block.bool_statement += f"\"{tok.value}\""
                    self.__advance()
                elif tok.type_ == TT_CHAR:
                    bool_block.bool_statement += f"'{tok.value}'"
                    self.__advance()
                elif tok.type_ == TT_ID and tok.value in self.VARS:
                    bool_block.bool_statement += str(self.__expr())
                elif tok.type_ == TT_KAND:
                    bool_block.bool_statement += "&"
                    self.__advance()
                elif tok.type_ == TT_NOT:
                    bool_block.bool_statement += " !"
                    self.__advance()
                elif tok.type_ == TT_EQ:
                    bool_block.bool_statement += " == "
                    self.__advance()
                elif tok.type_ == TT_NEQ:
                    bool_block.bool_statement += " != "
                    self.__advance()
                elif tok.type_ == TT_LTHEN:
                    bool_block.bool_statement += " < "
                    self.__advance()
                elif tok.type_ == TT_GTHEN:
                    bool_block.bool_statement += " > "
                    self.__advance()
                elif tok.type_ == TT_LEQ:
                    bool_block.bool_statement += " <= "
                    self.__advance()
                elif tok.type_ == TT_GEQ:
                    bool_block.bool_statement += " >= "
                    self.__advance()
                elif tok.type_ == TT_AND:
                    bool_block.bool_statement += " && "
                    self.__advance()
                elif tok.type_ == TT_OR:
                    bool_block.bool_statement += " || "
                    self.__advance()
                elif tok.type_ == TT_RPAREN:
                    self.__advance()
                    break
                else:
                    NewError("IllegalBoolStatement", "An illegal bool statement was found: ", tok)
            
            if self.__current_token.type_ == TT_LCURL:
                code_block = CodeBlock()
                self.__advance()
                while self.__current_token.type_ != TT_RCURL:
                    code_block = self.__check_and_make_type(code_block)
                self.__advance()
            else:
                NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            return WhileNode(bool_block, code_block)
    def __for(self):
        self.__advance()
        if self.__current_token.type_ == TT_LPAREN:
            self.__advance()
            if self.__current_token.value == "int":
                cnt_init = self.__assign(self.__current_token.value)
            elif self.__current_token.value == "flt":
                cnt_init = self.__assign(self.__current_token.value)
            elif self.__current_token.value == "str":
                cnt_init = self.__assign(self.__current_token.value)
            elif self.__current_token.value == "char":
                cnt_init = self.__assign(self.__current_token.value)
            else:
                cnt_init = self.__call_or_refference()
            if self.__current_token.type_ == TT_SEMIC:
                self.__advance()
                bool_block = BoolNode()
                while self.__current_token.type_ != TT_EOF:
                    tok = self.__current_token
                    if tok.type_ in (TT_INT, TT_FLOAT):
                        bool_block.bool_statement += str(tok.value)
                        self.__advance()
                    elif tok.type_ == TT_STRING:
                        bool_block.bool_statement += f"\"{tok.value}\""
                        self.__advance()
                    elif tok.type_ == TT_CHAR:
                        bool_block.bool_statement += f"'{tok.value}'"
                        self.__advance()
                    elif tok.type_ == TT_ID and tok.value in self.VARS:
                        bool_block.bool_statement += str(self.__expr())
                    elif tok.type_ == TT_KAND:
                        bool_block.bool_statement += "&"
                        self.__advance()
                    elif tok.type_ == TT_NOT:
                        bool_block.bool_statement += " !"
                        self.__advance()
                    elif tok.type_ == TT_EQ:
                        bool_block.bool_statement += " == "
                        self.__advance()
                    elif tok.type_ == TT_NEQ:
                        bool_block.bool_statement += " != "
                        self.__advance()
                    elif tok.type_ == TT_LTHEN:
                        bool_block.bool_statement += " < "
                        self.__advance()
                    elif tok.type_ == TT_GTHEN:
                        bool_block.bool_statement += " > "
                        self.__advance()
                    elif tok.type_ == TT_LEQ:
                        bool_block.bool_statement += " <= "
                        self.__advance()
                    elif tok.type_ == TT_GEQ:
                        bool_block.bool_statement += " >= "
                        self.__advance()
                    elif tok.type_ == TT_AND:
                        bool_block.bool_statement += " && "
                        self.__advance()
                    elif tok.type_ == TT_OR:
                        bool_block.bool_statement += " || "
                        self.__advance()
                    elif tok.type_ == TT_RPAREN:
                        self.__advance()
                        break
                    else:
                        NewError("IllegalBoolStatement", "An illegal bool statement was found: ", tok)
                if self.__current_token.type_ == TT_LCURL:
                    code_block = CodeBlock()
                    self.__advance()
                    while self.__current_token.type_ != TT_RCURL:
                        code_block = self.__check_and_make_type(code_block)
                    self.__advance()
                else:
                    NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            else:
                NewError("NoSemicolonFoundButExpected")
            return ForNode(cnt_init, bool_block, code_block)

    # needs types
    def __mk_id(self):
        tok = self.__current_token
        if self.__func_on:
            if tok.value == "return":
                node = self.__call_or_refference()
                return node
        if tok.value == "int":
            node = self.__assign(tok.value)
        elif tok.value == "flt":
            node = self.__assign(tok.value)
        elif tok.value == "str":
            node = self.__assign(tok.value)
        elif tok.value == "char":
            node = self.__assign(tok.value)
        elif tok.value == "cock":
            node = self.__assign(tok.value)
        elif tok.value == "uint8":
            node = self.__assign(tok.value)
        elif tok.value == "uint16":
            node = self.__assign(tok.value)
        elif tok.value == "uint32":
            node = self.__assign(tok.value)
        elif tok.value == "uint64":
            node = self.__assign(tok.value)
        elif tok.value == "int8":
            node = self.__assign(tok.value)
        elif tok.value == "int16":
            node = self.__assign(tok.value)
        elif tok.value == "int32":
            node = self.__assign(tok.value)
        elif tok.value == "int64":
            node = self.__assign(tok.value)
        elif tok.value in CUSTOM_TYPES:
            node = self.__assign(tok.value)
        elif tok.value == "mikf":
            node = self.__mikf()
        elif tok.value == "struct":
            node = self.__struct()
        elif tok.value == "estruct":
            node = self.__struct(True)
        elif tok.value == "mikas":
            node = self.__mikas()
        elif tok.value == "if":
            node = self.__if()
        elif tok.value == "else":
            node = self.__else()
        elif tok.value == "elif":
            node = self.__elif()
        elif tok.value == "while":
            node = self.__while()
        elif tok.value == "for":
            node = self.__for()
        else:
            node = self.__call_or_refference()
        return node


"""
- WORKS -
lexer = Lexer("int hallo = 1+2*5+4*1+2")
parser = Parser(lexer.lex())
root = parser.parse()
print(root.nodes[0])
"""
#with open("../test.mik", "r") as f:
#    cntnt = f.read()

#processed = preprocess(cntnt, "test.mik")
#lexer, sections = Lexer(processed).lex()
#print(sections)
#parser = Parser(lexer)
#root = parser.parse()
#print(root.nodes)