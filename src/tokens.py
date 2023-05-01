from dataclasses import dataclass

token_type = str

ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Types
PARENT = "PARENT"
CHILD  = "CHILD"
PARAM  = "PARAM"

# Operators
ASSIGN = "="

# Delimiters
LSQBRA = "["
RSQBRA = "]"
SLASH = "/"
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
TEMPLATE = "TEMPLATE"

VALUE = "VALUE"
TYPE  = "TYPE"
PROMPT = "PROMPT"
SRC = "SRC"
FONT_SIZE = "FONT_SIZE"
ROLE = "ROLE"


@dataclass
class Token:
    """Class for a token"""
    type: token_type 
    literal: str

PARENT_KEYWORDS = {
    "document": DOCUMENT,
    "meta": META,
    "data": DATA,
}

CHILD_KEYWORDS = {
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
    "template": TEMPLATE,
}

PARAMS_KEYWORDS = {
    "value": VALUE,
    "type": TYPE,
    "prompt": PROMPT,
    "src": SRC,
    "font_size": FONT_SIZE,
    "role": ROLE,
}

KEYWORDS = {
    **PARENT_KEYWORDS,
    **CHILD_KEYWORDS,
    **PARAMS_KEYWORDS,
}

def lookup_literal_type(literal: str) -> token_type:
    if literal.strip() in PARENT_KEYWORDS:
        return PARENT
    elif literal.strip() in CHILD_KEYWORDS:
        return CHILD
    elif literal.strip() in PARAMS_KEYWORDS:
        return PARAM
    else:
        return ILLEGAL