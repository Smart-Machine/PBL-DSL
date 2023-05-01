from src import lexer
from src import tokens
from src import parsers_utils
from scripts.bundling import bundle_html
from scripts.renderer import print_output, render


class Parser:

    current_token: tokens.Token
    next_token: tokens.Token
    lexer: lexer.Lexer
    program: dict
    parser_funcs: dict

    def __init__(self, lexer: lexer.Lexer) -> None:
        self.current_token = None
        self.next_token = None
        self.lexer = lexer
        self.program = {}

        self.read_token()
        self.read_token()

        self.parser_funcs = {
            1: parsers_utils.process_basic,
            # 2: ...
        }

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
                    literal = self.current_token.literal.split('=')
                    name, value = literal[0], "".join(literal[1:]) 
                    params[name] = value.replace("'", "")
                    self.read_token()
                working_path.append({
                    "node": tok.literal,
                    "params": params,
                })

            self.read_token()
        return self.program

    def evaluate(self, program: dict) -> None:
        template_model = 0
        output_file_name = None
        output_file_format = None

        try:
            meta_components = program.get("body")[0].get("body")
            for component in meta_components:
                if component.get("node") == "template":
                    if component.get("params").get("value") == "1":
                        template_model = 1
                        if output_file_name:
                            bundle_html("templates/basic", output_file_name)
                        else:
                            bundle_html("templates/basic")
                    elif component.get("params").get("value") == "2":
                        # TODO: add more templates
                        bundle_html("template/...")
                if component.get("node") == "name":
                    output_file_name = component.get("params").get("value")
                if component.get("node") == "format":
                    output_file_format = component.get("params").get("value")

        except Exception as e:
            print("An error occured when processing [meta] section.")
            return

        try:
            data_components = program.get("body")[1].get("body")
            for component in data_components:
                if output_file_name:
                    self.parser_funcs[template_model](
                        component, output_file_name 
                    )
                else:
                    self.parser_funcs[template_model](
                        component
                    )
        except Exception as e:
            print("An error occured when processing [data] section.")
            print(e)

        if output_file_format and output_file_name:
            render(output_file_name, output_file_format)
        elif output_file_name:
            render(file_name=output_file_name)
        elif output_file_format:
            render(file_format=output_file_format)
        else:
            render()
