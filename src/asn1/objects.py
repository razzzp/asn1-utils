from typing import List
from asn1.utils import *

class ASN1Root:
    def __init__(self, type : str) -> None:
        self.type = type
        self.is_optional = True

    def as_asn1_str(self) -> str:
        # to be overriden
        raise NotImplementedError(f'as_asn1_str() is not implemented in {self.__class__}')


class ASN1Object (ASN1Root):
    def __init__(self, type : str, value = None) -> None:
        super().__init__(type)
        self.value = value

    def as_asn1_str(self, indent = 0) -> str:
        return f'{indent_str(indent)}{self.type} ::= {self.value}'
    
class ASN1Sequence (ASN1Root):
    def __init__(self) -> None:
        super().__init__('sequence')
        self.children : List[ASN1Root] = []

    def as_asn1_str(self, indent = 0) -> str:
        result = f'{indent_str(indent)}{self.type} :: = {{\n'
        for child in self.children:
            result += child.as_asn1_str(indent+1) + '\n'
        result += indent_str(indent) + '}'
        return result