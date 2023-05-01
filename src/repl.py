import json
from src import lexer
from src import parsers
from src import tokens 

PROMPT = ">> "

def start(display_tokens: bool = False, display_parse_tree: bool = False) -> None:
    while True:
        print(PROMPT, end="")
        inp = input()
        if inp == "quit":
            return 
        
        if display_tokens:
            l = lexer.Lexer(inp)
            tok = l.next_token()
            while tok.type != tokens.EOF:
                print(tok)
                tok = l.next_token()
        if display_parse_tree:
            l = lexer.Lexer(inp)
            p = parsers.Parser(l)
            print(json.dumps(p.parse(), indent=4))
