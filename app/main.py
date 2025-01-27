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
        self.errors = []
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

                    self.LogError(f"[line {self.line}] Error: Unexpected character: {c}")
                    
            
        return #maybe return something
        
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
            self.LogError(f"[line {self.line}] Error: Unterminated string.")
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
    
    def HasErrors(self):
        return len(self.errors) > 0
    
    def PrintErrors(self):
        for error in self.errors:
            print(error, file=sys.stderr)

    def LogError(self, error):
        self.errors.append(error)


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


class Parser:

    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens
        self.errors = []
        self.expr = ""

    def Parse(self):
        resultexpr = self.Equality()
        self.expr = resultexpr if resultexpr != None else "" 

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

        while self.Match("GREATER") or self.Match("GREATER_EQUAL") or self.Match("LESS") or self.Match("LESS_EQUAL"):
            operator = self.Previous()
            right = self.Term()
            
            
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Term(self):
        expr = self.Factor()
        while self.Match("MINUS") or self.Match("PLUS"):
            operator = self.Previous()
            right = self.Factor()
            if right is None:
                self.LogError("Empty group")
                return None
            expr = Expr.Binary(expr, operator, right)
        
        return expr
    
    def Factor(self):
        expr = self.Unary()
        while self.Match("SLASH") or self.Match("STAR"):
            operator = self.Previous()
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
            if expr is None:
                self.LogError("Empty Group")
                return None
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
        self.LogError(message)

    def Check(self, type):
        if self.atEnd(): 
            return False
        return self.Peek().token_type == type
    
    def HasErrors(self):
        return len(self.errors) > 0
    
    def PrintErrors(self):
        for error in self.errors:
            print(error, file=sys.stderr)

    def LogError(self, error):
        self.errors.append(f"Error: {error}")
    
    def PrintExpr(self):
        print(self.expr)

class RuntimeError:

    def __init__(self, token, message):
        self.token = token
        self.message = message

class Interpreter:

    def __init__(self, expr):
        self.expr = expr
        self.errors = []
    
    def Interpret(self):
        try:
            value = self.Evaluate(self.expr)
            print(self.Stringify(value))

        except RuntimeError as error:
            self.RuntimeError(error)
            
    
    def Stringify(self, obj):
        if obj == None: return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text[-2:] == ".0": #this might be wrong
                text = text[:-2] #might be wrong
            
            return text
        
        return str(obj)
    def HasErrors(self):
        return len(self.errors) > 0

    def RuntimeError(self, error):
        self.errors.append(error)
        print(error.message + f"\n[line {error.token.line}]", file=sys.stderr) #may be wrong

    def VisitLiteralExpr(self, expr):
        if expr.value is None: return "nil"
        if expr == True: return "true"
        if expr == False: return "false"
        return (str(expr.value)).lower()

    def VisitGroupingExpr(self, expr):
        return self.Evaluate(expr.expression)
    
    def VisitUnaryExpr(self, expr):
        right = self.Evaluate(expr.right)

        match expr.oparator.type:
            case "MINUS":
                self.CheckNumberOperand(expr.operator, right)
                return -float(right)
            case "BANG":
                return "false" if self.IsTruthy(right) == "true" else "true"

        return "nil"
    
    def VisitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case "MINUS":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) - float(right)
            case "SLASH":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) / float(right)
            case "STAR":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) * float(right)
            case "PLUS":
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                
                raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case "GREATER":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) > float(right)
            case "GREATER_EQUAL":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) >= float(right)
            case "LESS":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) < float(right)
            case "LESS_EQUAL":
                self.CheckNumberOperands(self, expr.operator, left, right)
                return float(left) <= float(right)
            case "BANG_EQUAL":
                return "false" if self.IsEqual(left, right) == True else "true"
            case "EQUAL":
                return self.IsEqual(left, right)

        return "nil"
    

    def CheckNumberOperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operand must be numbers.") # this might not work

    def CheckNumberOperand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.") # this might not work
    
    def IsEqual(self, a, b):
        if a == None and b == None: return "true"
        if a == None: return "false"

        return "true" if a == b else "false"
    
    def IsTruthy(self, obj):
        if obj == None: return "false"
        if isinstance(obj, bool): return obj
        return "true"

    def Evaluate(self, expr):
        if isinstance(expr, Expr.Literal):
            return self.VisitLiteralExpr(expr)
        elif isinstance(expr, Expr.Grouping):
            return self.Evaluate(expr.expression)
        elif isinstance(expr, Expr.Unary):
            return self.VisitUnaryExpr(expr)
        elif isinstance(expr, Expr.Binary):
            return self.VisitBinaryExpr(expr)


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
            
            errorcode = 0

            Scannerx = Scanner(file_contents)
            Scannerx.ScanTokens()
            if Scannerx.HasErrors():
                Scannerx.PrintErrors()
                errorcode = 65

            Scannerx.PrintTokens()
            print("EOF  null")
            exit(errorcode) 

    elif command == "parse":
        with open(filename) as file:
            file_contents = file.read()

            if not file_contents:
                print("EOF  null") # Placeholder, remove this line when implementing the scanner
                return 0

            errorcode = 0

            Scannerx = Scanner(file_contents)
            Scannerx.ScanTokens()
            if Scannerx.HasErrors():
                Scannerx.PrintErrors()
                errorcode = 65
            

            Parserx = Parser(Scannerx.tokens)
            Parserx.Parse()
            if Parserx.HasErrors():
                Parserx.PrintErrors()
                errorcode = 65
            Parserx.PrintExpr()
            
            exit(errorcode)
    
    elif command == "evaluate":
        with open(filename) as file:
            file_contents = file.read()

            if not file_contents:
                print("EOF  null") # Placeholder, remove this line when implementing the scanner
                return 0

            errorcode = 0

            Scannerx = Scanner(file_contents)
            Scannerx.ScanTokens()
            if Scannerx.HasErrors():
                Scannerx.PrintErrors()
                errorcode = 65
            

            Parserx = Parser(Scannerx.tokens)
            Parserx.Parse()
            if Parserx.HasErrors():
                Parserx.PrintErrors()
                errorcode = 65
            
            Interpreterx = Interpreter(Parserx.expr)
            Interpreterx.Interpret()
            if Interpreterx.HasErrors():
                errorcode = 70
            
            exit(errorcode)


    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)



    print("Logs from your program will appear here!", file=sys.stderr)



if __name__ == "__main__":
    main()
