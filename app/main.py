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
                        continue
                    elif self.IsAlpha(c):
                        self.Identifier()
                        continue

                    print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
                    self.error_code = 65
            
        return self.error_code
        
    def Identifier(self):
        while self.IsAlphaNumeric(self.Peek()):
            self.Advance()

        text = self.source[self.start:self.current]
        if text not in self.keywords.keys():
            self.AddToken("IDENTIFIER", None)
        else:
            self.AddToken(self.keywords[text], None)

    def atEnd(self):
        return self.current >= len(self.source)

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


class Expr:
    class Literal:
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return "nil" if self.value is None else str(self.value).lower()

    class Unary: 
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right

        def __str__(self):
            return f"({self.operator.lexeme} {self.right})".lower()

    class Binary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

        def __str__(self):
            return f"({self.operator.lexeme} {self.left} {self.right})".lower()
    
    class Grouping:
        def __init__(self, expression):
            self.expression = expression

        def __str__(self):
            return f"(group {self.expression})".lower()


class Parser():

    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens

    def Parse(self):
        return self.Equality()

    def Expression(self):
        return self.Equality()
    
    def Equality(self):
        expr = self.Comparison()

        while self.Match("BANG_EQUAL") or self.Match("EQUAL_EQUAL"):
            operator = self.Previous()
            right = self.Comparison()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Comparison(self):
        expr = self.Term()
        print(f"Entered Comparison with initial expr: {expr}", file=sys.stderr)

        while self.Match("GREATER") or self.Match("GREATER_EQUAL") or self.Match("LESS") or self.Match("LESS_EQUAL"):
            operator = self.Previous()
            right = self.Term()
            
            
            print(f"Operator: {operator}, Type: {type(operator)}", file=sys.stderr)
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Term(self):
        expr = self.Factor()
        while self.Match("MINUS") or self.Match("PLUS"):
            operator = self.Previous()
            right = self.Factor()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Factor(self):
        expr = self.Unary()
        while self.Match("SLASH") or self.Match("STAR"):
            operator = self.Previous
            right = self.Unary()
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Unary(self):
        if self.Match("BANG") or self.Match("MINUS"):
            operator = self.Previous()
            right = self.Unary()
            return Expr.Unary(operator, right)
        
        return self.Primary()
    
    def Primary(self):
        if self.Match("FALSE"): return Expr.Literal(False)
        if self.Match("TRUE"): return Expr.Literal(True)
        if self.Match("NIL"): return Expr.Literal(None)

        if self.Match("NUMBER") or self.Match("STRING"):
            return Expr.Literal(self.Previous().literal)
        
        if self.Match("LEFT_PAREN"):
            expr = self.Expression()
            self.Consume("RIGHT_PAREN", "Expect ')' after expression.")
            return Expr.Grouping(expr)

    def Advance(self):
        if self.atEnd():
            return '\0'
        char = self.tokens[self.current]
        self.current += 1
        return char


    def Match(self, expected):
        if self.atEnd():
            return False
        if self.tokens[self.current].token_type != expected:
            return False

        self.current += 1
        return True
    
    def atEnd(self):
        return self.current >= len(self.tokens)
    
    def Previous(self):
        return self.tokens[self.current - 1]
    
    def Peek(self):
        if self.atEnd(): return None
        return self.tokens[self.current]

    def Consume(self, type, message):
        if self.Check(type): 
            return self.Advance()

        raise Exception(f"[line {self.Peek().line}] {message}")

    def Check(self, type):
        if self.atEnd(): 
            return False
        return self.Peek().token_type == type

    






def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]



    if command == "tokenize":
        
        with open(filename) as file:
            file_contents = file.read()

            if not file_contents:
                print("EOF  null") # Placeholder, remove this line when implementing the scanner
                return 0

            Scannerx = Scanner(file_contents)
            exitcode = Scannerx.ScanTokens()

            Scannerx.PrintTokens()
            print("EOF  null")
            exit(exitcode) 

    elif command == "parse":
        with open(filename) as file:
            file_contents = file.read()

            if not file_contents:
                print("EOF  null") # Placeholder, remove this line when implementing the scanner
                return 0


            Scannerx = Scanner(file_contents)
            Scannerx.ScanTokens()

            Parserx = Parser(Scannerx.tokens)
            print(Parserx.Parse())
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)



    print("Logs from your program will appear here!", file=sys.stderr)



if __name__ == "__main__":
    main()
