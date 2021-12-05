from io import StringIO
from sys import stdout
from enum import Enum
from typing import List

class TokenType (Enum):
    IDENTIFIER = 0,
    KEYWORD = 1,
    SEPARATOR = 2,
    OPERATOR = 3,
    LITERAL = 4,

class Token:
    def __init__(self, value : str, type : TokenType, name : str = '') -> None:
        self.value = value
        self.type = type
        self.name = name
        pass

class LexerState (Enum):
    START = 0
    IN_LEXEME = 1 
    IN_WHITESPACE = 2

Keywords = {
    'ABSENT',
    'ABSTRACT-SYNTAX',
    'ALL',
    'APPLICATION',
    'AUTOMATIC',
    'BEGIN',
    'BIT',
    'BMPString',
    'BOOLEAN',
    'BY',
    'CHARACTER',
    'CHOICE',
    'CLASS',
    'COMPONENT',
    'COMPONENTS',
    'CONSTRAINED',
    'CONTAINING',
    'DATE',
    'DATE-TIME',
    'DEFAULT',
    'DEFINITIONS',
    'DURATION',
    'EMBEDDED',
    'ENCODED',
    'ENCODING-CONTROL',
    'END',
    'ENUMERATED',
    'EXCEPT',
    'EXPLICIT',
    'EXPORTS',
    'EXTENSIBILITY',
    'EXTERNAL',
    'FALSE',
    'FROM',
    'GeneralizedTime',
    'GeneralString',
    'GraphicString',
    'IA5String',
    'IDENTIFIER',
    'IMPLICIT',
    'IMPLIED',
    'IMPORTS',
    'INCLUDES',
    'INSTANCE',
    'INSTRUCTIONS',
    'INTEGER',
    'INTERSECTION',
    'ISO646String',
    'MAX',
    'MIN',
    'MINUS-INFINITY',
    'NOT-A-NUMBER',
    'NULL',
    'NumericString',
    'OBJECT',
    'ObjectDescriptor',
    'OCTET',
    'OF',
    'OID-IRI',
    'OPTIONAL',
    'PATTERN',
    'PDV',
    'PLUS-INFINITY',
    'PRESENT',
    'PrintableString',
    'PRIVATE',
    'REAL',
    'RELATIVE-OID',
    'RELATIVE-OID-IRI',
    'SEQUENCE',
    'SET',
    'SETTINGS',
    'SIZE',
    'STRING',
    'SYNTAX',
    'T61String',
    'TAGS',
    'TeletexString',
    'TIME',
    'TIME-OF-DAY',
    'TRUE',
    'TYPE-IDENTIFIER',
    'UNION',
    'UNIQUE',
    'UNIVERSAL',
    'UniversalString',
    'UTCTime',
    'UTF8String',
    'VideotexString',
    'VisibleString',
    'WITH',   
}

MultiCharSymbol = {
    '.' : 'dot',
    ':' : 'colon',
    '[' : 'start_square_brace',
    ']' : 'end_square_brace',
    '*' : 'asterik',
    '/' : 'forward_slash',
    '-' : 'hypen'
    # </ and /> not supported
}

MultiCharSymbolLexemes ={
    '..' : 'double_dot',
    '[[' : 'double_start_square_brace',
    ']]' : 'double_end_square_brace',
    '/*' : 'start comment',
    '*/' : 'end_comment',
    '--' : 'single line comment'
}

SingleCharSymbol = {
    '=' : 'equals',
    '\'' : 'quote',
    '\"' : 'double_quotes',
    ',' : 'comma',
    # hypens can be in identifiers
    #'-' : 'hypen',
    #'/' : 'slash',
    #':' : 'colon',
    ';' : 'semi_colon',
    '@' : 'at',
    '|' : 'pipe',
    '!' : 'exclamation',
    '^' : 'caret',
     '(' : 'start_brace',
    '{' : 'start_curly_brace',
    #'[' : 'start_square_brace',
    '<' : 'less_than',
     ')' : 'end_brace',
    '}' : 'end_curly_brace',
    #']' : 'end_square_brace',
    '>' : 'greater_than',
}

WhiteSpace = {
    ' ' : 'space',
    '\n' : 'newline',
    '\t' : 'tab'
}

class Lexer:
    pass

class ASN1Lexer (Lexer):
    def __init__(self) -> None:
        super().__init__()
        self._state = LexerState.START
        self._tokens : List[str] = []
        self._cur_lexeme = ''

    def tokenize(self, istream : StringIO):
        lexemes = self._get_lexemes(istream)
        #
        tokens = self._get_tokens(lexemes)
        return tokens

    def _get_lexemes(self, istream : StringIO) -> List[str]:
        result = []
        prev_char = ' '
        cur_char = ''
        cur_lexeme = ''

        while True:
            cur_char = istream.read(1)
            if cur_char == '':
                if cur_lexeme != '':
                    result.append(cur_lexeme)
                break
            # state machine
            if prev_char.isalnum() and prev_char not in WhiteSpace:
            # prev char is alpha-numeric
                if cur_char in WhiteSpace:
                    # end of current lexeme, append and reset
                    result.append(cur_lexeme)
                    cur_lexeme=''

                elif cur_char in MultiCharSymbol:
                    # if multi char symbol, just append lexeme
                    # don't append cur char
                    if cur_char != '-':
                        result.append(cur_lexeme)
                        cur_lexeme = cur_char
                    else:
                        # single hypen can be part of identifier
                        # continue
                        cur_lexeme += cur_char
                elif cur_char in SingleCharSymbol:
                    # if prev_char not whitespace, and cur_char is single char lexeme
                    # end of cur_lexeme                   
                    result.append(cur_lexeme)
                    cur_lexeme= ''
                    # also add the cur char as lexeme
                    result.append(cur_char)
                elif cur_char not in WhiteSpace:
                    # prev_char not whitespace & cur_char is whitespace
                    # continue adding chars
                    cur_lexeme += cur_char
            elif prev_char in MultiCharSymbol:
                cur_symbol = prev_char + cur_char
                if cur_symbol in MultiCharSymbolLexemes:
                    # case comment after alpha num
                    if cur_symbol == '--' and len(cur_lexeme) > 2:
                        # identifier is everthing except last char ('-')
                        result.append(cur_lexeme[0:-1])
                    result.append(cur_symbol)
                    cur_lexeme=''
                elif cur_char == '=' and cur_lexeme == '::':
                    cur_lexeme += cur_char
                    result.append(cur_lexeme)
                    cur_lexeme=''
                elif cur_char == ':' and prev_char == ':':
                    # continue
                    cur_lexeme += cur_char
                elif cur_char == '.' and cur_lexeme == '..':
                    cur_lexeme += cur_char
                    result.append(cur_lexeme)
                    cur_lexeme=''
                else:
                    if cur_char in SingleCharSymbol:
                        result.append(cur_lexeme)
                        result.append(cur_char)
                    elif cur_char not in WhiteSpace:
                        cur_lexeme += cur_char
                # TODO comments
            else:
                if cur_char in SingleCharSymbol:
                    if cur_lexeme != '':
                        result.append(cur_lexeme)
                        cur_lexeme = ''
                    result.append(cur_char)     
                elif cur_char not in WhiteSpace:
                    # prev_char not whitespace & cur_char is whitespace
                    cur_lexeme += cur_char
            prev_char = cur_char
        return result

    def _get_tokens(self, lexemes : List[str]) -> List[Token]:
        result = []
        for (i, lexeme) in enumerate(lexemes):
            # TODO
            result.append(lexeme)
            pass
        return result
    
    def _next_state(self, input : str, state : LexerState) -> LexerState:
        if WhiteSpace[input]:
            return LexerState.IN_WHITESPACE
        else:
            return LexerState.IN_LEXEME

