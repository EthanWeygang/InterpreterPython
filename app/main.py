import sys

class Token:

    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
    
    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal != None else "null"}"



class Scanner:

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_code = 0
    
    def atEnd(self):
        return self.current <= len(self.source)

    def ScanTokens(self):
        while not self.atEnd():
            start = self.current
            c = self.Advance()

            match c:
                case '(': self.AddToken("LEFT_PAREN", c); break
                case ')': self.AddToken("RIGHT_PAREN", c); break
                case '{': self.AddToken("LEFT_BRACE", c); break
                case '}': self.AddToken("RIGHT_BRACE", c); break
                case ',': self.AddToken("COMMA", c); break
                case '.': self.AddToken("DOT", c); break
                case '-': self.AddToken("MINUS", c); break
                case '+': self.AddToken("PLUS", c); break
                case ';': self.AddToken("SEMICOLON", c); break
                case '*': self.AddToken("STAR", c); break
                case '!': self.AddToken("BANG_EQUAL" if self.Match("=") else "BANG")
                case '=': self.AddToken("EQUAL_EQUAL" if self.Match("=") else "EQUAL")
                case '<': self.AddToken("LESS_EQUAL" if self.Match("=") else "LESS")
                case '>': self.AddToken("GREATER_EQUAL" if self.Match("=") else "GREATER")
                case "\n": line += 1; break
                case _: 
                    print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
                    self.error_code = 65; break
            

        self.PrintTokens()
        print("EOF  null")
        return self.error_code
        

    def Advance(self):
        self.current += 1
        return self.source[self.current]
    
    def AddToken(self, type, literal):
        self.tokens.append(Token(type, self.source[self.start:self.current + 1], literal))
    
    def PrintTokens(self):
        for t in self.tokens:
            print(t)
    
    def Match(self, expected):
        if self.atEnd:
            return False
        if self.source[self.current + 1] != expected: return False
        
        current += 1
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
