import tokens


class Lexer:

    source: str
    current_index: int
    next_index: int
    char: str

    def __init__(self, source: str, current_index: int = 0, next_index: int = 0, char: str = "") -> None:
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
        while self.char == " " or self.char == "\t" or self.char == "\r":
            self.read_char()

    def read_component_name(self) -> str:
        pos = self.current_index
        while self.is_letter(self.char):
            self.read_char()
        return self.source[pos:self.current_index]

    def is_letter(self, char: str) -> bool:
        return 'a' <= char and char <= 'z' or 'A' <= char and char <= 'Z' or char == '_'

    def read_string(self) -> str:
        pos = self.current_index
        while self.char != "\"":
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
            case "=":
                tok = tokens.Token(tokens.ASSIGN, self.char)
            case "\"":
                self.read_char()
                literal = self.read_string()
                type = tokens.STRING
                self.read_char()
                return tokens.Token(type, literal)
            case 0:
                tok = tokens.Token(tokens.EOF, "")
            case _:
                if self.is_letter(self.char):
                    literal = self.read_component_name()
                    type = tokens.lookup_component_type(literal)
                    return tokens.Token(type, literal)
                else:
                    tok = tokens.Token(tokens.ILLEGAL, self.char)

        self.read_char()
        return tok
