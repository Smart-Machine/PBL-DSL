import lexer
import tokens

PROMPT = ">> "

def start() -> None:
    while True:
        print(PROMPT, end="")
        inp = input()
        if inp == "quit":
            return

        l = lexer.Lexer(inp)  

        tok = l.next_token()
        while tok.type != tokens.EOF:
            print(tok)
            tok = l.next_token()