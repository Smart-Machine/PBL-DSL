import lexer
import tokens


class Parser:

    current_token: tokens.Token
    next_token: tokens.Token
    lexer: lexer.Lexer
    program: dict

    def __init__(self, lexer: lexer.Lexer) -> None:
        self.current_token = None
        self.next_token = None
        self.lexer = lexer
        self.program = {}

        self.read_token()
        self.read_token()

    def read_token(self) -> tokens.Token:
        self.current_token = self.next_token
        self.next_token = self.lexer.next_token()

    def parse(self) -> dict:
        working_path = None
        while self.current_token.type != tokens.EOF:
            if self.current_token.type in ["[", "]"]:
                self.read_token()
                continue

            if not self.program and self.current_token.type == tokens.PARENT and self.current_token.literal == "document" and working_path == None:
                self.program["node"] = self.current_token.literal
                self.program["body"] = []
            elif self.current_token.type == tokens.PARENT:
                self.program["body"].append({
                    "node": self.current_token.literal, 
                    "body": [], 
                })
                for i, element in enumerate(self.program["body"]):
                    if element["node"] == self.current_token.literal:
                        working_path = self.program["body"][i]["body"]
                        break
            elif self.current_token.type == tokens.CHILD:
                tok = self.current_token
                self.read_token()
                params = {}
                while self.current_token.type == tokens.PARAM:
                    name, value = self.current_token.literal.split('=')
                    params[name] = value.replace("'", "")
                    self.read_token()
                working_path.append({
                    "node": tok.literal,
                    "params": params, 
                })

            self.read_token()
        return self.program