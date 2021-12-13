from enum import Enum
from typing import Dict, List, Tuple
from asn1.lexers import Token
from asn1.asn1_schema import ASN1Schema, ASN1SchemaValue
from asn1.dicts import *
from src.asn1.asn1_schema import ASN1SchemaDefinitions

class _ParserState(Enum):
    INITIAL = 0,
    DEFINITIONS = 1,
    ASSIGNMENTS = 2

class _ContextKey (Enum):
    STATE = 0,
    MODULE_IDENTIFIER = 1

class ASN1Parser:
    def parse(self, tokens : List[Token]) -> ASN1Schema:
        schema = ASN1Schema()
        state =  _ParserState.INITIAL
        tokens_toprocess = []

        for token in tokens:
            if state == _ParserState.INITIAL:
                # getting module identiifer
                if token.value == 'DEFINITIONS':
                    # change state and set identifier in schema
                    state = _ParserState.DEFINITIONS
                    schema.module_identifier = ASN1ModuleIdentifierParser().parse(tokens_toprocess) # parse
                    tokens_toprocess.clear()
                else:
                    # appends to list to process
                    tokens_toprocess.append(token)
                return
            if state == _ParserState.DEFINITIONS:
                if token.value == 'BEGIN':
                    # change state and set identifier in schema
                    state = _ParserState.ASSIGNMENTS
                    schema.definitions = ASN1DefinitionsParser().parse(tokens_toprocess) # parse
                    tokens_toprocess.clear()
                else:
                    # appends to list to process
                    tokens_toprocess.append(token)
                return
            if state == _ParserState.ASSIGNMENTS:
                return
        return schema

class ASN1ModuleIdentifierParser:
    def parse(self, tokens : List[Token]) -> ASN1SchemaValue:
        result = ''
        for token in tokens:
            result += token.value
        return result

class ASN1DefinitionsParser:
    def parse(self, tokens : List[Token]) -> ASN1SchemaDefinitions:
        result = ASN1SchemaDefinitions()
        # TODO
        return result