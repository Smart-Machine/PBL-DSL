from src import tokens


class Lexer:

    source: str
    current_index: int
    next_index: int
    char: str

    def __init__(
        self,
        source: str,
        current_index: int = 0,
        next_index: int = 0,
        char: str = ""
    ) -> None:
        self.source = source
        self.current_index = current_index
        self.next_index = next_index
        self.char = char

        self.read_char()

    def new_token(self, token_type: tokens.token_type, ch: str) -> tokens.Token:
        return tokens.Token(token_type, ch)

    def read_char(self) -> None:
        if self.next_index >= len(self.source):
            self.char = 0
        else:
            self.char = self.source[self.next_index]
        self.current_index = self.next_index
        self.next_index += 1

    def skip_whitespace(self) -> None:
        while self.char == " " or self.char == "\t" or self.char == "\r" or self.char == "\n":
            self.read_char()

    def is_letter(self, char: str) -> bool:
        return 'a' <= char and char <= 'z' or 'A' <= char and char <= 'Z' or char == '_'

    def read_literal(self) -> str:
        pos = self.current_index
        while self.is_letter(self.char):
            self.read_char()
        return self.source[pos:self.current_index]

    def read_param(self) -> str:
        if self.char != "=":
            raise Exception("Expected an equal sign")

        self.read_char()

        if self.char != "\"":
            raise Exception("Expected string as param value")

        self.read_char()

        pos = self.current_index
        while self.char != "\"" and self.char != tokens.EOF:
            self.read_char()
        return self.source[pos:self.current_index]

    def next_token(self) -> tokens.Token:
        tok = None

        self.skip_whitespace()

        match self.char:
            case "[":
                tok = tokens.Token(tokens.LSQBRA, self.char)
            case "]":
                tok = tokens.Token(tokens.RSQBRA, self.char)
            case 0:
                tok = tokens.Token(tokens.EOF, "")
            case _:
                if self.is_letter(self.char):
                    literal = self.read_literal()
                    type = tokens.lookup_literal_type(literal)
                    if type == tokens.PARAM:
                        param = self.read_param()
                        if param:
                            self.read_char()
                            return tokens.Token(type, f"{literal}='{param}'")
                    return tokens.Token(type, literal)
                else:
                    tok = tokens.Token(tokens.ILLEGAL, self.char)

        self.read_char()
        return tok
