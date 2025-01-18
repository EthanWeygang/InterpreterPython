import sys

class Token:

    def __init__(self, token_type, lexeme, literal=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
    
    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal if self.literal != None else "null"}"

def ParseContents(text):
    error_code = 0
    line = 1

    for c in text:
        match c:
            case '(': print(Token("LEFT_PAREN", c)); continue
            case ')': print(Token("RIGHT_PAREN", c)); continue
            case '{': print(Token("LEFT_BRACE", c)); continue
            case '}': print(Token("RIGHT_BRACE", c)); continue
            case ',': print(Token("COMMA", c)); continue
            case '.': print(Token("DOT", c)); continue
            case '-': print(Token("MINUS", c)); continue
            case '+': print(Token("PLUS", c)); continue
            case ';': print(Token("SEMICOLON", c)); continue
            case '*': print(Token("STAR", c)); continue
            case "\n": line += 1
            case _: 
                print(f"[line {line}] Error: Unexpected character: {c}", file=sys.stderr)
                error_code = 65
        
        

    print("EOF  null")
    return error_code

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
        exit(ParseContents(file_contents))
        
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner




if __name__ == "__main__":
    main()
