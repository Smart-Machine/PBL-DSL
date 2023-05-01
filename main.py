import json
import sys
from src import repl
from src import lexer
from src import tokens
from src import parsers


def main():
    display_tokens = False
    display_parse_tree = False
    display_evaluate = False
    if "--tokens" in sys.argv:
        display_tokens = True
    if "--parse-tree" in sys.argv:
        display_parse_tree = True
    if "--evaluate" in sys.argv:
        display_evaluate = True

    if len(sys.argv) > 1:
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

            if display_evaluate:
                l = lexer.Lexer(source)
                p = parsers.Parser(l)
                p.evaluate(p.parse())
    else:
        repl.start(display_tokens, display_parse_tree)


if __name__ == "__main__":
    main()
