from compiler_util.preprocessor import *
from compiler_util.lexer import *
from compiler_util.error import *

TYPES = [
    "int",
    "flt",
    "str",
    "char"
]
INSTRUCTIONS = [
    "int",
    "flt",
    "str",
    "char",
    "mikf",
    "mikas",
    "struct",
    "bool"
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

    def __repr__(self) -> str:
        return f"{self.tok}"

class StrNode:
    def __init__(self, tok) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f"{self.tok}"

class CharNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    
    def __repr__(self) -> str:
        return f"{self.tok}"

class TypeNode:
    def __init__(self, tok) -> None:
        self.tok = tok
    def __repr__(self) -> str:
        return f"{self.tok}"

class IDNode:
    def __init__(self, var_name, tok) -> None:
        self.tok = tok
    
    def __repr__(self) -> str:
        return f"{self.tok}"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.right_node = right_node
        self.op_tok = op_tok
    
    def __repr__(self) -> str:
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnaryOpNode:
    def __init__(self) -> None:
        pass

class AsignmentNode:
    def __init__(self, type_, pointer, name, op=None, value=None) -> None:
        self.type_ = type_
        self.pointer = pointer
        self.name = name
        self.value = value
        self.op = op
    
    def __repr__(self) -> str:
        return f"({self.type_} {self.name} {self.op} {self.value})"

class ArgBlockNode:
    def __init__(self) -> None:
        self.bool_bl_list = []
    def add_arg(self, node):
        self.bool_bl_list.append(node)
    
    def __repr__(self) -> str:
        return f"{self.bool_bl_list}"

class CodeBlock:
    def __init__(self) -> None:
        self.code_bl_list = []

    def add_arg(self, node):
        self.code_bl_list.append(node)
    
    def __repr__(self) -> str:
        return f"{self.code_bl_list}"

class FunctionNode:
    def __init__(self, function_name, return_type, arg_block: ArgBlockNode, code_block: CodeBlock) -> None:
        self.func_name = function_name
        self.ret_type = return_type
        self.arg_block = arg_block
        self.code_block = code_block
    
    def __repr__(self) -> str:
        return f"({self.func_name} ({self.arg_block}) -> {self.ret_type} {self.code_block})"

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

# NODES END


class Parser:
    def __init__(self, tokens: list) -> None:
        self.__tokens = tokens
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

    def __check_and_make_type(self, node):
        if self.__current_token.type_ in (TT_INT, TT_FLOAT):
            res = self.__expr()
            node.add_arg(res)
        elif self.__current_token.type_ == TT_ID:
            res = self.__mk_id()
            node.add_arg(res)
        else:
            None

        return node

    def parse(self):
        while self.__current_token.type_ != TT_EOF:
            if self.__current_token.type_ in (TT_INT, TT_FLOAT):
                res = self.__expr() # gets tree for mathematical expr
                self.__programm_node.add_node(res)
            elif self.__current_token.type_ == TT_ID:
                res = self.__mk_id()
                self.__programm_node.add_node(res)
            elif self.__current_token.type_ == TT_DEBUG:
                self.__programm_node.add_node(DebugNode(TT_DEBUG))
                self.__advance()
            else:
                break

        return self.__programm_node

    def __factor(self):
        tok = self.__current_token

        if tok.type_ in (TT_INT, TT_FLOAT):
            self.__advance()
            return NumberNode(tok)
        
        elif tok.type_ in (TT_ID):
            if tok.value in self.VARS:
                tok2 = self.VARS.get(tok.value)
                tok2 = tok.value
            elif tok.value in self.FUNCTIONS:
                tok2 = self.FUNCTIONS.get(tok.value)
                tok2 = tok.value
            else:
                NewError("RefferencedBeforeAssignement", f"The variable '{tok.value}' is refferenced but not assigned!")
            self.__advance()
            return IDNode(tok.value, tok2)
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
    def __assign(self, type_):
        self.__advance()
        if self.__current_token.type_ == TT_MUL:
            pointer = True
            self.__advance()
        else:
            pointer = False
        if self.__current_token.type_ == TT_ID:
            name = self.__current_token.value
            if name in self.VARS:
                NewError("VariableNameDuplicate", f"The variable: {name} is already defined!")
            self.__advance()
            # should be = now
            if self.__current_token.type_ == TT_ASSGN:
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
                            elif self.__current_token.type_ == TT_COMMA:
                                self.__advance()
                                continue
                            else:
                                node = self.__mk_id()
                            new_block.append(node)
                        self.__advance()
                        if len_args != len(new_block):
                            NewError("ParameterExpectedError", f"{len_args} args were expected but {len(new_block)} args were found!", f"-> Section {new_block[0].tok.section} at Line {new_block[0].tok.ln_count}")
                        else:
                            return AsignmentNode(type_, pointer, name, asgn_op, FunctionCall(f_name, new_block))
                else:
                    value = self.__expr()
                    self.VARS.update({name:AsignmentNode(type_, pointer, name, asgn_op, value)})
                    return AsignmentNode(type_, pointer, name, asgn_op, value)
            else:
                self.VARS.update({name:AsignmentNode(type_, pointer, name)})
                return AsignmentNode(type_, pointer, name)
    def __call_or_refference(self):
        call = self.__current_token
        call_name = self.__current_token.value

        if call.type_ in (TT_INT, TT_FLOAT, TT_STRING, TT_CHAR):
            node = self.__factor()
        else:
            self.__advance()
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
                    elif self.__current_token.type_ == TT_COMMA:
                        self.__advance()
                        continue
                    else:
                        node2 = self.__mk_id()
                    new_block.append(node2)
                if len_args != len(new_block):
                    NewError("ParameterExpectedError", f"{len_args} args were expected but {len(new_block)} args were found!", f"-> Section {new_block[0].tok.section} at Line {new_block[0].tok.ln_count}")
                else:
                    node = FunctionCall(call_name, new_block)
                self.__advance()
            elif self.__current_token.type_ == TT_ASSGN:
                self.__advance()
                if self.__current_token.type_.lower() == (self.VARS.get(call_name)).type_:
                    node = AsignmentNode(type_=(self.VARS.get(call_name)).type_, name=call_name, op="=", value=self.__current_token)
                else:
                    NewError("TypeMissmatchException", f"The variable you are trying to assign has type: {(self.VARS.get(call_name)).type_} but you tried to assign: {self.__current_token.type_.lower()}")
                self.__advance()
            elif call.value == "return":
                node = ReturnNode(self.__factor())
            elif self.__current_token.type_ not in (TT_LPAREN, TT_ASSGN, TT_EOF, TT_LCURL, TT_RCURL, TT_INT, TT_COMMA, TT_FLOAT, TT_STRING, TT_CHAR):
                if self.__current_token.value in self.VARS:
                    #inf = self.VARS.get(self.__current_token.value)
                    #inf = inf.value
                    #node = ReferenceNode(inf)
                    node = IDNode(self.__current_token.value, self.__current_token.value)
                else:
                    NewError("VarOrFunctionNotFound", f"The var name refferenced is not defined: {self.__current_token}")
                self.__advance()
            else:
                NewError("RefferenceError", self.__current_token)
        return node
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
                        else:
                            NewError("InvalidTypeError", f"You specified an invalid type in function decleration: {self.__current_token}")
                        bool_block_node.add_arg(node)
                self.__advance()
                if self.__current_token.type_ == TT_ARROW:
                    self.__advance()
                    if self.__current_token.value in TYPES:
                        ret_type = self.__current_token.value
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
                else:
                    NewError("NoCodeBlockError", "No Code block '{}' was started but one was expected")
            self.VARS = old_vars
            self.FUNCTIONS.update({f"{func_name}":FunctionNode(func_name, ret_type, bool_block_node, code_block)})
            return FunctionNode(func_name, ret_type, bool_block_node, code_block)
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
                        else:
                            NewError("InvalidTypeError", f"You specified an invalid type in function decleration: {self.__current_token}")
                        bool_block_node.add_arg(node)
                self.__advance()
                if self.__current_token.type_ == TT_ARROW:
                    self.__advance()
                    if self.__current_token.value in TYPES:
                        ret_type = self.__current_token.value
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
        elif tok.value == "mikf":
            node = self.__mikf()
        elif tok.value == "struct":
            pass
        elif tok.value == "mikas":
            node = self.__mikas()
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
