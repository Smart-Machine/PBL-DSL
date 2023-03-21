import json
import sys
import repl
import lexer
import tokens
import parsers

def main():
    display_tokens = False
    display_parse_tree = False
    if "--tokens" in sys.argv:
        display_tokens = True
    if "--parse-tree" in sys.argv:
        display_parse_tree = True

    if len(sys.argv) > 3:
        with open(sys.argv[1], "r") as file:
            source = file.read()
            if display_tokens:
                l = lexer.Lexer(source)

                tok = l.next_token()
                while tok.type != tokens.EOF:
                    print(tok)
                    tok = l.next_token()
            if display_parse_tree:
                l = lexer.Lexer(source)
                p = parsers.Parser(l)
                print(json.dumps(p.parse(), indent=4))
    else:
        repl.start(display_tokens, display_parse_tree)

if __name__=="__main__":
    main()