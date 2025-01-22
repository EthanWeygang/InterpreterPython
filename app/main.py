import sys

class Token:

    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
    
    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal != None else 'null'}"



class Scanner:

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_code = 0
        self.keywords = {
                "and":   "AND",
                "class": "CLASS",
                "else":  "ELSE",
                "false": "FALSE",
                "for":   "FOR",
                "fun":   "FUN",
                "if":    "IF",
                "nil":   "NIL",
                "or":    "OR",
                "print": "PRINT",
                "return":"RETURN",
                "super": "SUPER",
                "this":  "THIS",
                "true":  "TRUE",
                "var":   "VAR",
                "while": "WHILE"
        }
    
    def atEnd(self):
        return self.current >= len(self.source)

    def ScanTokens(self):
        while not self.atEnd():
            self.start = self.current
            c = self.Advance()

            match c:
                case '(': self.AddToken("LEFT_PAREN", None)
                case ')': self.AddToken("RIGHT_PAREN", None)
                case '{': self.AddToken("LEFT_BRACE", None)
                case '}': self.AddToken("RIGHT_BRACE", None)
                case ',': self.AddToken("COMMA", None)
                case '.': self.AddToken("DOT", None)
                case '-': self.AddToken("MINUS", None)
                case '+': self.AddToken("PLUS", None)
                case ';': self.AddToken("SEMICOLON", None)
                case '*': self.AddToken("STAR", None)
                case '!': self.AddToken("BANG_EQUAL" if self.Match("=") else "BANG", None)
                case '=': self.AddToken("EQUAL_EQUAL" if self.Match("=") else "EQUAL", None)
                case '<': self.AddToken("LESS_EQUAL" if self.Match("=") else "LESS", None)
                case '>': self.AddToken("GREATER_EQUAL" if self.Match("=") else "GREATER", None)
                case '/': 
                    if not self.Match("/"):
                        self.AddToken('SLASH', None)
                        continue

                    while not self.atEnd() and self.Peek() != '\n':
                        self.Advance()
                case '"': self.String()
                case ' ': continue
                case '\r': continue
                case '\t': continue
                case "\n": self.line += 1
                case _: 
                    if self.IsDigit(c):
                        self.Number()
                        print(c,file=sys.stderr)
                        continue
                    elif self.IsAlpha(c):
                        self.Identifier()
                        continue

                    print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
                    self.error_code = 65
            

        self.PrintTokens()
        print("EOF  null")
        return self.error_code
        
    def Identifier(self):
        while self.IsAlphaNumeric(self.Peek()):
            self.Advance()

        text = self.source[self.start:self.current]
        if text not in self.keywords.keys():
            self.AddToken("IDENTIFIER", None)
        else:
            self.AddToken(self.keywords[text], self.keywords[text])


    def String(self):
        while self.Peek() != '"' and not self.atEnd():
            if self.Peek() == "\n": self.line += 1
            self.Advance()
        
        if self.atEnd():
            print(f"[line {self.line}] Error: Unterminated string.",file=sys.stderr)
            self.error_code = 65
            return

        self.Advance()

        value = self.source[self.start+1:self.current - 1]
        self.AddToken("STRING", value)

    def Number(self):
        while self.IsDigit(self.Peek()):
            self.Advance()

            if self.Peek() == "." and self.IsDigit(self.PeekNext()):
                self.Advance()
            
                while self.IsDigit(self.Peek()):
                    self.Advance()
                
        self.AddToken("NUMBER", float(self.source[self.start: self.current]))

    def IsDigit(self, c):
        return  c is not None and c.isdigit()
    
    def IsAlpha(self, c):
        return c  is not None and (c.isalpha() or c in "_")

    def IsAlphaNumeric(self, c):
        return self.IsDigit(c) or self.IsAlpha(c)

    def Advance(self):
        if self.atEnd():
            return '\0'
        char = self.source[self.current]
        self.current += 1
        return char


    def Peek(self):
        if self.atEnd(): return None
        return self.source[self.current]
    
    def PeekNext(self):
        if self.current + 1 >= len(self.source): return None
        return self.source[self.current + 1]

    
    def AddToken(self, token_type, literal):
        self.tokens.append(Token(token_type, self.source[self.start:self.current], literal))


    def PrintTokens(self):
        for t in self.tokens:
            print(t)
    

    def Match(self, expected):
        if self.atEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True









def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]



    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()



    print("Logs from your program will appear here!", file=sys.stderr)



    if file_contents:
        Scannerx = Scanner(file_contents)
        exit(Scannerx.ScanTokens())
        
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner




if __name__ == "__main__":
    main()
