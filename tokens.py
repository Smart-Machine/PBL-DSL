from dataclasses import dataclass

token_type = str

ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Types
STRING = "STRING"

# Operators
ASSIGN = "="

# Delimiters
LSQBRA = "["
RSQBRA = "]"
DBLQUOTE = "\""
NEWLINE = "\n"

# Keywords
DOCUMENT = "DOCUMENT"
META = "META"
DATA = "DATA"
NAME = "NAME"
FORMAT = "FORMAT"
PATH = "PATH"
SIZE = "SIZE"
DATE = "DATE"
AUTHOR = "AUTHOR"
TITLE = "TITLE"
TEXT = "TEXT"
IMAGE = "IMAGE"
BARCODE = "BARCODE"
BATCH_NUMBER = "BATCH_NUMBER"

VALUE = "VALUE"
TYPE  = "TYPE"
PROMPT = "PROMPT"
SRC = "SRC"
FONT_SIZE = "FONT_SIZE"


@dataclass
class Token:
    """Class for a token"""
    type: token_type 
    literal: str

KEYWORDS = {
    "document": DOCUMENT,
    "meta": META,
    "data": DATA,
    "name": NAME,
    "format": FORMAT,
    "path": PATH,
    "size": SIZE,
    "date": DATE,
    "author": AUTHOR,
    "title": TITLE,
    "text": TEXT,
    "image": IMAGE,
    "barcode": BARCODE,
    "batch_number": BATCH_NUMBER,
    "value": VALUE,
    "type": TYPE,
    "prompt": PROMPT,
    "src": SRC,
    "font_size": FONT_SIZE,
}

def lookup_component_type(literal: str) -> token_type:
    if KEYWORDS.get(literal.strip(), False):
        return KEYWORDS[literal.strip()]
    return ILLEGAL