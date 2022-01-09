from enum import Enum
from typing import Dict, List, Tuple
from asn1.lexers import Token
from asn1.schema import ASN1Schema, ASN1SchemaAssignmentList, ASN1SchemaValue, ASN1SchemaDefinitions
from asn1.dicts import *

class _ParserState(Enum):
    INITIAL = 0,
    DEFINITIONS = 1,
    ASSIGNMENTS = 2,
    END = 3

class _ContextKey (Enum):
    STATE = 0,
    MODULE_IDENTIFIER = 1

def _raise_unexpectedtoken(token : Token):
    raise ValueError(f'unexpected token \'{token.value}\'. line {token.line_num}')

class ASN1Parser:
    def parse(self, tokens : List[Token]) -> ASN1Schema:
        schema = ASN1Schema()
        state =  _ParserState.INITIAL
        tokens_toprocess = []

        for token in tokens:
            if state == _ParserState.INITIAL:
                # getting module identiifer
                if token.value == 'DEFINITIONS':
                    # change state, parse identifier and set in schema
                    state = _ParserState.DEFINITIONS
                    schema.module_identifier = ASN1ModuleIdentifierParser().parse(tokens_toprocess)
                    tokens_toprocess.clear()
                else:
                    # appends to list to process
                    tokens_toprocess.append(token)
            elif state == _ParserState.DEFINITIONS:
                if token.value == 'BEGIN':
                    # change state, parse definitions and set in schema
                    state = _ParserState.ASSIGNMENTS
                    schema.definitions = ASN1DefinitionsParser().parse(tokens_toprocess)
                    tokens_toprocess.clear()
                else:
                    # appends to list to process
                    tokens_toprocess.append(token)
            elif state == _ParserState.ASSIGNMENTS:
                if token.value == 'END':
                    # change state, parse definitions and set in schema
                    state = _ParserState.END
                    # TODO
                    schema.assignment_list =  ASN1SchemaAssignmentList()
                    tokens_toprocess.clear()
                else:
                    # appends to list to process
                    tokens_toprocess.append(token)
            else:
                # TODO
                pass
        if state != _ParserState.END:
            raise EOFError('unexpected EOF')
        return schema

class ASN1ModuleIdentifierParser:
    def parse(self, tokens : List[Token]) -> ASN1SchemaValue:
        # TODO break down the identifier
        result = ''
        for token in tokens:
            result += token.value
        return ASN1SchemaValue(result)

class ASN1DefinitionsParser:
    def parse(self, tokens : List[Token]) -> ASN1SchemaValue:
        result = ASN1SchemaDefinitions()
        accum = ''
        state = 0 if 'INSTRUCTIONS' in tokens else 1
        for token in tokens:
            if state == 0:
                # encoding default
                if token.value == 'INSTRUCTIONS':
                    # next state
                    result.encoding_default = ASN1SchemaValue(accum + token.value)
                    accum = ''
                    state = 1
                else:
                    accum += token.value
            elif state == 1:
                # tag default
                if token.value in ('EXPLICIT', 'IMPLICIT', 'AUTOMATIC'):
                    accum += token.value
                elif token.value == 'TAGS':
                    if accum != '':
                        # next state
                        result.tag_default = ASN1SchemaValue(accum + ' ' +token.value)
                        accum =''
                        state = 2
                    else:
                        _raise_unexpectedtoken(token)
                else:
                    state = 2
            elif state == 2: 
                # extension default
                if token.value == 'EXTENSIBILITY':
                    accum += token.value
                elif token.value == 'IMPLIED' and accum == 'EXTENSIBILITY':
                    result.extension_default = ASN1SchemaValue(accum +' '+ token.value)
                    accum = ''
                    state = 3
                else:
                    _raise_unexpectedtoken(token)
            elif state == 3:
                if token.value == '::=':
                    state = -1
                else:
                    _raise_unexpectedtoken(token)
            else:
                _raise_unexpectedtoken(token)
        return result

    class ASN1AssignmentsListParser:
        def parse(self, tokens : List[Token]) -> ASN1SchemaValue:
            result = ASN1SchemaAssignmentList()


            pass
