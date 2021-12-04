from compiler_util.error import NewError


CHARS       = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
NUMBERS     = "0123456789"


TT_LTHEN    = "LTHEN"
TT_GTHEN    = "GTHEN"
TT_LEQ      = "LEQ"
TT_GEQ      = "GEQ"
TT_AND      = "AND"
TT_OR       = "OR"
TT_NEQ      = "NEQ"
TT_NOT      = "NOT"

TT_KAND     = "KAND"
TT_DOT      = "DOT"

TT_PLUS     = "PLS"
TT_MINUS    = "MIN"
TT_MUL      = "MUL"
TT_DIV      = "DIV"
TT_INT      = "INT"
TT_FLOAT    = "FLT"
TT_ID       = "ID"
TT_STRING   = "STR"
TT_CHAR     = "CHAR"
TT_ASSGN    = "ASSGN"
TT_REASGN   = "REASGN"
TT_EQ       = "EQUALS"
TT_LPAREN   = "LPAREN"
TT_RPAREN   = "RPAREN"
TT_LBRK     = "LBRK"
TT_RBRK     = "RBRK"
TT_LCURL    = "LCURL"
TT_RCURL    = "RCURL"
TT_COMMA    = "COMMA"
TT_ARROW    = "ARROW"
TT_SEMIC    = "SEMICOLON"
TT_PERCENT  = "PERCENT"
TT_DEBUG    = "DEBUG"
TT_OVERRIDE = "OVERRIDE"
TT_EOF      = "EOF"

class Position:
    def __init__(self, prev=None, section=None) -> None:
        self.prev = prev
        self.section = section
        self.ln_cnt = 0
    
    def __repr__(self) -> str:
        return f"File or Section: {self.section} at Line: {self.ln_cnt}"

class Token:
    def __init__(self, type_, section, ln_cnt, value=None) -> None:
        self.section = section
        self.ln_count = ln_cnt
        self.type_ = type_
        self.value = value
    
    def __repr__(self) -> str:
        return f"Token: {self.type_} value: {self.value} In {self.section} at ln {self.ln_count}"


class Lexer:
    def __init__(self, text: str) -> None:
        self.__text: str = text
        self.__pos: int = -1
        self.__current_char: chr = None
        self.__sec: Position = None
        self.__expect_mikas = False
        self.__in_mikas = False
        self.__advance()

    def __advance(self):
        self.__pos += 1
        self.__current_char = self.__text[self.__pos] if self.__pos < len(self.__text) else None
    
    def lex(self):
        tokens = []
        sections = []
        while self.__current_char != None:
            if self.__in_mikas:
                tokens.append(self.__make_str())
                self.__advance()
                self.__in_mikas = False
            elif self.__current_char in " \t\n":
                if self.__current_char == "\n":
                    self.__sec.ln_cnt += 1
                self.__advance()
            
            elif self.__current_char == ".":
                tokens.append(Token(TT_DOT, self.__sec.section, self.__sec.ln_cnt, "."))
                self.__advance()

            elif self.__current_char == "[":
                tokens.append(Token(TT_LBRK, self.__sec.section, self.__sec.ln_cnt, "["))
                self.__advance()
            
            elif self.__current_char == "]":
                tokens.append(Token(TT_RBRK, self.__sec.section, self.__sec.ln_cnt, "]"))
                self.__advance()

            elif self.__current_char == ";":
                tokens.append(Token(TT_SEMIC, self.__sec.section, self.__sec.ln_cnt, ";"))
                self.__advance()

            elif self.__current_char == "?":
                self.__advance()
                if self.__current_char == "=":
                    tokens.append(Token(TT_REASGN, self.__sec.section, self.__sec.ln_cnt, "?="))
                    self.__advance()

            elif self.__current_char == "!":
                self.__advance()
                if self.__current_char == "=":
                    tokens.append(Token(TT_NEQ, self.__sec.section, self.__sec.ln_cnt, "!="))
                    self.__advance()
                else:
                    tokens.append(Token(TT_NOT, self.__sec.section, self.__sec.ln_cnt, "!"))

            elif self.__current_char == "&":
                self.__advance()
                if self.__current_char == "&":
                    tokens.append(Token(TT_AND, self.__sec.section, self.__sec.ln_cnt, "&&"))
                    self.__advance()
                else:
                    tokens.append(Token(TT_KAND, self.__sec.section, self.__sec.ln_cnt, "&"))
            
            elif self.__current_char == "|":
                self.__advance()
                if self.__current_char == "|":
                    tokens.append(Token(TT_OR, self.__sec.section, self.__sec.ln_cnt, "||"))
                    self.__advance()
                else:
                    NewError("IllegalTokenError", f"A token was found but not expected: bare |. In: ", self.__sec)

            elif self.__current_char == "%":
                tokens.append(Token(TT_PERCENT, self.__sec.section, self.__sec.ln_cnt, "%"))
                self.__advance()

            elif self.__current_char == "+":
                tokens.append(Token(TT_PLUS, self.__sec.section, self.__sec.ln_cnt, "+"))
                self.__advance()
            
            elif self.__current_char == "*":
                tokens.append(Token(TT_MUL, self.__sec.section, self.__sec.ln_cnt, "*"))
                self.__advance()
            
            elif self.__current_char == "/":
                self.__advance()
                if self.__current_char == "/":
                    while self.__current_char != "\n" and self.__current_char != None:
                        self.__advance()
                elif self.__current_char == "*":
                    self.__advance()
                    while True:
                        if self.__current_char == "*":
                            self.__advance()
                            if self.__current_char == "/":
                                self.__advance()
                                break
                        self.__advance()
                else:
                    tokens.append(Token(TT_DIV, self.__sec.section, self.__sec.ln_cnt, "/"))
            
            elif self.__current_char in NUMBERS:
                tokens.append(self.__make_number())
            
            elif self.__current_char in CHARS:
                tokens.append(self.__make_id())
            
            elif self.__current_char == "<":
                self.__advance()
                if self.__current_char == "=":
                    tokens.append(Token(TT_LEQ, self.__sec.section, self.__sec.ln_cnt, "<="))
                    self.__advance()
                else:
                    tokens.append(Token(TT_LTHEN, self.__sec.section, self.__sec.ln_cnt, "<"))
            
            elif self.__current_char == ">":
                self.__advance()
                if self.__current_char == "=":
                    tokens.append(Token(TT_GEQ, self.__sec.section, self.__sec.ln_cnt, ">="))
                    self.__advance()
                else:
                    tokens.append(Token(TT_GTHEN, self.__sec.section, self.__sec.ln_cnt, ">"))

            elif self.__current_char == "=":
                self.__advance()
                if self.__current_char == "=":
                    tokens.append(Token(TT_EQ, self.__sec.section, self.__sec.ln_cnt, "=="))
                    self.__advance()
                else:
                    tokens.append(Token(TT_ASSGN, self.__sec.section, self.__sec.ln_cnt, "="))
            
            elif self.__current_char == "\"":
                tokens.append(self.__make_str())
                self.__advance()
            
            elif self.__current_char == "'":
                tokens.append(self.__make_char())
                self.__advance()
            
            elif self.__current_char == "(":
                tokens.append(Token(TT_LPAREN, self.__sec.section, self.__sec.ln_cnt, "("))
                self.__advance()
            
            elif self.__current_char == ")":
                tokens.append(Token(TT_RPAREN, self.__sec.section, self.__sec.ln_cnt, ")"))
                self.__advance()
            
            elif self.__current_char == "{":
                if self.__expect_mikas:
                    self.__in_mikas = True
                    self.__expect_mikas = False
                tokens.append(Token(TT_LCURL, self.__sec.section, self.__sec.ln_cnt,"{"))
                self.__advance()
            
            elif self.__current_char == "}":
                tokens.append(Token(TT_RCURL, self.__sec.section, self.__sec.ln_cnt, "}"))
                self.__advance()
            
            elif self.__current_char == ",":
                tokens.append(Token(TT_COMMA, self.__sec.section, self.__sec.ln_cnt, ","))
                self.__advance()
            
            elif self.__current_char == "-":
                self.__advance()
                if self.__current_char == ">":
                    tokens.append(Token(TT_ARROW, self.__sec.section, self.__sec.ln_cnt, "->"))
                    self.__advance()
                else:
                    tokens.append(Token(TT_MINUS, self.__sec.section, self.__sec.ln_cnt, "-"))

            elif self.__current_char == "@":
                self.__advance()
                if self.__current_char in CHARS:
                    id_str = ""

                    while self.__current_char != None and self.__current_char in CHARS+NUMBERS:
                        id_str += self.__current_char
                        self.__advance()
                    comp_flg_kind = id_str
                    if comp_flg_kind == "section":
                        if self.__current_char == "(":
                            self.__advance()
                            if self.__current_char == "\"":
                                mk_str = ""
                                self.__advance()
                                while self.__current_char != None and self.__current_char != "\"":
                                    mk_str += self.__current_char
                                    self.__advance()
                                sec_name = mk_str
                                self.__advance()
                                if self.__current_char == ")":
                                    if self.__sec != None:
                                        if self.__sec.ln_cnt > 1:
                                            self.__sec.ln_cnt -= 1
                                    self.__sec = Position(prev=self.__sec ,section=sec_name)
                                    sections.append(sec_name)
                                    self.__advance()
                                else:
                                    NewError("ParenteseNotClosed", "In a compiler flag, a closing parentese was expected")
                            else:
                                NewError("CompilerFlagSectionColumnExpectedButNotFound", "A '\"' was expected but not found in a @section()")
                        else:
                            NewError("OpeningParenteseExpected", "In a compiler flag, a opening parentese was expected")
                    elif comp_flg_kind == "secend":
                        self.__sec = self.__sec.prev
                        self.__advance()
                    elif comp_flg_kind == "debug":
                        tokens.append(Token(TT_DEBUG, self.__sec.section, self.__sec.ln_cnt))
                        self.__advance()
                    elif comp_flg_kind == "override":
                        tokens.append(Token(TT_OVERRIDE, self.__sec.section, self.__sec.ln_cnt))
                        self.__advance()
                    else:
                        NewError("InvalidCompilerFlag", "An invalid compiler flag was specified")
                else:
                    NewError("NoCompilerFlagArgumentError", "After a '@' something like 'section' is expected but not found")
            else:
                print(f"UnidentifiedTokenError: '{self.__current_char}'")
                quit()
        #for i in tokens:
        #    print(i)
        #    print()
        tokens.append(Token(TT_EOF, "none", "none"))
        return tokens, sections

    def __make_char(self):
        self.__advance()
        char = ""
        if self.__current_char != "'":
            char += self.__current_char
            self.__advance()
            if self.__current_char == "'":
                return Token(TT_CHAR, self.__sec.section, self.__sec.ln_cnt, char)
            else:
                NewError("CharStatementNotEnded", "You started a char in single qoutes but didn't close them after one char!")
        else:
            return Token(TT_CHAR, self.__sec.section, self.__sec.ln_cnt, char)

    def __make_str(self):
        mk_str = ""
        if self.__in_mikas:
            cnt = 0
            while self.__current_char != None and self.__current_char != "}":
                if self.__current_char == "\n" and cnt > 0:
                    mk_str += ";"
                elif self.__current_char == "\n" and cnt <= 0:
                    None
                elif self.__current_char == "\t":
                    None
                else:
                    mk_str += self.__current_char
                self.__advance()
                cnt += 1
            return Token(TT_STRING, self.__sec.section, self.__sec.ln_cnt, mk_str)
        else:
            self.__advance()
            while self.__current_char != None and self.__current_char != "\"":
                mk_str += self.__current_char
                self.__advance()
            return Token(TT_STRING, self.__sec.section, self.__sec.ln_cnt, mk_str)

    def __make_number(self):
        num_str = ""
        dot_count = 0

        while self.__current_char != None and self.__current_char in NUMBERS + ".":
            if self.__current_char == ".":
                if dot_count == 1: break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.__current_char
            self.__advance()

        if dot_count:
            return Token(TT_FLOAT, self.__sec.section, self.__sec.ln_cnt, float(num_str))
        else:
            return Token(TT_INT, self.__sec.section, self.__sec.ln_cnt, int(num_str))
    
    def __make_id(self):
        id_str = ""

        while self.__current_char != None and self.__current_char in CHARS+NUMBERS:
            id_str += self.__current_char
            self.__advance()
        if id_str == "mikas": self.__expect_mikas = True
        return Token(TT_ID, self.__sec.section, self.__sec.ln_cnt, str(id_str))
