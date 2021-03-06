from io import StringIO
from sys import stdout
from enum import Enum
from typing import List, TextIO
from asn1.dicts import *
from asn1.utils import *

class TokenType (Enum):
    UNDEFINED = -1,
    IDENTIFIER = 0,
    KEYWORD = 1,
    SEPARATOR = 2,
    OPERATOR = 3,
    LITERAL = 4,
    COMMENT = 5

class Token:
    def __init__(self, value : str, type : TokenType = TokenType.UNDEFINED, line_num = 0) -> None:
        self.value = value
        self.type = type
        self.name = ''
        self.line_num = line_num
        pass

    def pretty_print(self, out : TextIO, indent : int = 0):
        out.write(indent_str(indent) + '{\n')
        #out.write(indent_str(indent+1) + f'name : {self.name}\n')
        out.write(indent_str(indent+1) + f'type : {self.type}\n')
        out.write(indent_str(indent+1) + f'value : {self.value}\n')
        out.write(indent_str(indent+1) + f'line : {self.line_num}\n')
        out.write(indent_str(indent) + '}\n')


class Lexer:
    # maybe this will be used
    pass

class ASN1Lexer (Lexer):
    def __init__(self) -> None:
        super().__init__()
        self._tokens : List[str] = []
        self._cur_lexeme = ''

    def tokenize(self, istream : StringIO):
        lexemes = self._get_lexemes_v2(istream)
        #
        tokens = self._get_tokens(lexemes)
        return tokens

    # @DeprecationWarning
    # def _get_lexemes(self, istream : StringIO) -> List[str]:
    #     """Deprecated because of spaghetti"""
    #     result = []
    #     prev_char = ' '
    #     cur_char = ''
    #     cur_lexeme = ''

    #     while True:
    #         cur_char = istream.read(1)
    #         if cur_char == '':
    #             if cur_lexeme != '':
    #                 result.append(cur_lexeme)
    #             break
    #         # state machine
    #         if prev_char.isalnum() and prev_char not in WhiteSpace:
    #         # prev char is alpha-numeric
    #             if cur_char in WhiteSpace:
    #                 # end of current lexeme, append and reset
    #                 result.append(cur_lexeme)
    #                 cur_lexeme=''

    #             elif cur_char in MultiCharSymbol:
    #                 # if multi char symbol, just append lexeme
    #                 # don't append cur char
    #                 if cur_char != '-':
    #                     result.append(cur_lexeme)
    #                     cur_lexeme = cur_char
    #                 else:
    #                     # single hypen can be part of identifier
    #                     # continue
    #                     cur_lexeme += cur_char
    #             elif cur_char in SingleCharSymbol:
    #                 # if prev_char not whitespace, and cur_char is single char lexeme
    #                 # end of cur_lexeme                   
    #                 result.append(cur_lexeme)
    #                 cur_lexeme= ''
    #                 # also add the cur char as lexeme
    #                 result.append(cur_char)
    #             elif cur_char not in WhiteSpace:
    #                 # prev_char not whitespace & cur_char is whitespace
    #                 # continue adding chars
    #                 cur_lexeme += cur_char
    #         elif prev_char in MultiCharSymbol:
    #             cur_symbol = prev_char + cur_char
    #             if cur_symbol in MultiCharSymbolLexemes:
    #                 # case comment after alpha num
    #                 if cur_symbol == '--' and len(cur_lexeme) > 2:
    #                     # identifier is everthing except last char ('-')
    #                     result.append(cur_lexeme[0:-1])
    #                 result.append(cur_symbol)
    #                 cur_lexeme=''
    #             elif cur_char == '=' and cur_lexeme == '::':
    #                 cur_lexeme += cur_char
    #                 result.append(cur_lexeme)
    #                 cur_lexeme=''
    #             elif cur_char == ':' and prev_char == ':':
    #                 # continue
    #                 cur_lexeme += cur_char
    #             elif cur_char == '.' and cur_lexeme == '..':
    #                 cur_lexeme += cur_char
    #                 result.append(cur_lexeme)
    #                 cur_lexeme=''
    #             else:
    #                 if cur_char in SingleCharSymbol:
    #                     result.append(cur_lexeme)
    #                     result.append(cur_char)
    #                 elif cur_char not in WhiteSpace:
    #                     cur_lexeme += cur_char
    #             # TODO comments
    #         else:
    #             if cur_char in SingleCharSymbol:
    #                 if cur_lexeme != '':
    #                     result.append(cur_lexeme)
    #                     cur_lexeme = ''
    #                 result.append(cur_char)     
    #             elif cur_char not in WhiteSpace:
    #                 # prev_char not whitespace & cur_char is whitespace
    #                 cur_lexeme += cur_char
    #         prev_char = cur_char
    #     return result

    def _get_lexemes_v2(self, istream : StringIO) -> List[str]:
        result = []
        prev_char = ' '
        cur_char = ''
        cur_lexeme = ''
        in_singleline_comment = False
        in_multiline_comment = False

        while True:
            cur_char = istream.read(1)
            if cur_char == '':
                # if empty means end of file
                if cur_lexeme != '':
                    result.append(cur_lexeme)
                break
            # state machine
            if in_multiline_comment or in_singleline_comment:
                # in comment block
                if in_multiline_comment and prev_char + cur_char == '*/':
                    in_multiline_comment = False
                    result.append(cur_lexeme + cur_char)
                    cur_lexeme =''
                elif in_singleline_comment and cur_char == '\n':
                    in_singleline_comment = False
                    result.append(cur_lexeme)
                    cur_lexeme =''
                else:
                    # still in comment continue
                    cur_lexeme += cur_char      
            elif cur_char in WhiteSpace:
                # if whitespace, whatever is in cur_lexeme is added if not empty
                if cur_lexeme != '':
                    result.append(cur_lexeme)
                    cur_lexeme = ''          
            elif cur_char in SingleCharSymbol:
                if cur_char == '=' and cur_lexeme == '::':
                    result.append('::=')
                    cur_lexeme = ''
                else:
                    if cur_lexeme != '':
                        result.append(cur_lexeme)
                        cur_lexeme = ''
                    # also append the Single Char Symbol
                    result.append(cur_char)              
            elif cur_char in MultiCharSymbol:
                combined = cur_lexeme + cur_char
                if combined[-2:] == '--':
                    # for case cur_lexeme = 'blabla-'        
                    prev_lexeme = cur_lexeme[0:-1]
                    if prev_lexeme != '':
                        result.append(prev_lexeme)
                    # start comment
                    in_singleline_comment = True
                    cur_lexeme = '--'
                    pass
                elif combined == '/*':
                    # append all except last char
                    prev_lexeme = cur_lexeme[0:-1]
                    if prev_lexeme != '':
                        result.append(prev_lexeme)
                    # start comment
                    in_multiline_comment = True
                    cur_lexeme = '/*'
                    pass
                elif combined == '::':
                    # add and continue
                    cur_lexeme += cur_char
                elif combined in MultiCharSymbolLexemes:
                    result.append(combined)
                    cur_lexeme = ''
                else:
                    # start new multi char lexeme
                    if cur_lexeme != '' and cur_char != '-':
                        result.append(cur_lexeme)
                        cur_lexeme = cur_char
                    else:
                        # continue
                        cur_lexeme += cur_char
            elif cur_char.isalnum():
                cur_lexeme += cur_char
            else:
                raise ValueError(f'unsupported char found at {istream.tell()}: \'{cur_char}\'')
            #
            # keep newlines for line number tracking
            if cur_char == '\n':
                result.append('\n')
            prev_char = cur_char
        return result

    def _get_tokens(self, lexemes : List[str]) -> List[Token]:
        result = []
        line_counter = 0
        for (i, lexeme) in enumerate(lexemes):
            # TODO
            if lexeme in Keywords:
                result.append(Token(lexeme, TokenType.IDENTIFIER, line_counter))
            elif lexeme in Separators:
                result.append(Token(lexeme, TokenType.SEPARATOR, line_counter))
            elif lexeme in Operators:
                result.append(Token(lexeme, TokenType.OPERATOR, line_counter))
            elif self._is_comment(lexeme):
                result.append(Token(lexeme, TokenType.COMMENT, line_counter))
            elif lexeme == '\n':
                # ignore newlines, but increment line_counter
                line_counter += 1
            elif self._is_valid_identifier(lexeme):
                # should be an identifier
                result.append(Token(lexeme, TokenType.IDENTIFIER, line_counter))
            elif self._is_literal(lexeme):
                result.append(Token(lexeme, TokenType.LITERAL, line_counter))
            else:
                raise ValueError('unknown element: ' + lexeme)
            pass
        return result


    def _is_comment(self, lexeme : str):
        first2chars = lexeme[0:2]
        if first2chars == '/*' or first2chars == '--':
            return True
        return False

    def _is_valid_identifier(self, lexeme : str):
        if lexeme[0].isnumeric():
            return False
        if self._contains_invalidchars(lexeme):
            return False
        return True

    def _contains_invalidchars(self, lexeme : str):
        # TODO implement invalid identifier character checking
        return False

    def _is_literal(self, lexeme : str):
        return True

    
