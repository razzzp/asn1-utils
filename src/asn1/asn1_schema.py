from typing import List, TextIO

from asn1.utils import indent_str

class ASN1SchemaRoot:
    def __init__(self) -> None:
        pass

    def add(self, item):
        raise NotImplementedError(f'add not implemented in {__class__}')

    def setval():
        raise NotImplementedError(f'setval not implemeneted in {__class__}')

    def prettyprint(self, out : TextIO, indent = 0):
        out.write(f'{indent_str(indent)}rettyprint not implemented {__class__}')

class ASN1Schema (ASN1SchemaRoot):
    def __init__(self) -> None:
        self.module_identifier : ASN1SchemaValue = None
        self.definitions : ASN1SchemaDefinitions = None
        self.assignment_list : ASN1SchemaAssignmentList = None

    def prettyprint(self, out : TextIO, indent = 0):
        out.write(indent_str(indent)+'module_identifier:\n')
        self.module_identifier.prettyprint(out, indent+1)
        out.write(indent_str(indent)+'definitions:\n')
        self.definitions.prettyprint(out, indent+1)
        out.write(indent_str(indent)+'assignment_list:\n')
        self.assignment_list.prettyprint(out, indent+1)

class ASN1SchemaDefinitions (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()
        self.encoding_default : ASN1SchemaValue = None
        self.tag_default : ASN1SchemaValue = None
        self.extension_default : ASN1SchemaValue = None

    def prettyprint(self, out : TextIO, indent = 0):
        out.write(indent_str(indent)+'{\n')
        if self.encoding_default != None:
            out.write(f'{indent_str(indent+1)}encoding_default: ')
            self.encoding_default.prettyprint(out)
        if self.tag_default != None:
            out.write(f'{indent_str(indent+1)}tag_default: ')
            self.tag_default.prettyprint(out)
        if self.extension_default != None:
            out.write(f'{indent_str(indent+1)}extension_default: ')
            self.extension_default.prettyprint(out)
        out.write(indent_str(indent)+'}\n')
        
class ASN1SchemaValue (ASN1SchemaRoot):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def prettyprint(self, out: TextIO, indent = 0):
        out.write(f'{indent_str(indent)}val({self.value})\n')

class ASN1SchemaAssignmentList (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()
        self.type_assignments = List[ASN1SchemaAssignment]
        self.value_assignments = List[ASN1SchemaAssignment]

class ASN1SchemaAssignment (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()

