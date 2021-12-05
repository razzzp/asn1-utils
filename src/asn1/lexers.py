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

SingleCharLexeme = {
    '=' : 'equal',
    '\'' : 'quote',
    '\"' : 'double_quotes',
    ',' : 'comma',
    '-' : 'hypen',
    '/' : 'slash',
    ':' : 'colon',
    ';' : 'semi_colon',
    '@' : 'at',
    '|' : 'pipe',
    '!' : 'exclamation',
    '^' : 'caret',
     '(' : 'start_brace',
    '{' : 'start_curly_brace',
    '[' : 'start_square_brace',
    '<' : 'less_than',
     ')' : 'end_brace',
    '}' : 'end_curly_brace',
    ']' : 'end_square_brace',
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
            if prev_char not in WhiteSpace and prev_char not in SingleCharLexeme:
                if cur_char in WhiteSpace:
                    result.append(cur_lexeme)
                    cur_lexeme=''
                elif cur_char in SingleCharLexeme:
                    # if prev_char not whitespace, and cur_char is single char lexeme
                    # add cur_lexeme and the cur char as lexeme
                    result.append(cur_lexeme)
                    result.append(cur_char)
                    cur_lexeme=''
                elif cur_char not in WhiteSpace:
                    # prev_char not whitespace & cur_char is whitespace
                    cur_lexeme += cur_char
            else:
                if cur_char in SingleCharLexeme:
                    result.append(cur_char)
                elif cur_char not in WhiteSpace:
                    # prev_char not whitespace & cur_char is whitespace
                    cur_lexeme += cur_char
                
            prev_char = cur_char
        return result

    def _get_tokens(self, lexemes : List[str]) -> List[Token]:
        result = []
        for (lexeme, i) in enumerate(lexemes):
            pass
        return lexemes
    
    def _next_state(self, input : str, state : LexerState) -> LexerState:
        if WhiteSpace[input]:
            return LexerState.IN_WHITESPACE
        else:
            return LexerState.IN_LEXEME

