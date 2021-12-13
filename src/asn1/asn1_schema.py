from typing import List, TextIO

class ASN1SchemaRoot:
    def __init__(self) -> None:
        pass

    def add(self, item):
        raise NotImplementedError(f'add not implemented in {__class__}')

    def setval():
        raise NotImplementedError(f'setval not implemeneted in {__class__}')

    def prettyprint(self, out : TextIO):
        out.write(f'prettyprint not implemented {__class__}')

class ASN1Schema (ASN1SchemaRoot):
    def __init__(self) -> None:
        self.module_identifier : ASN1SchemaValue = None
        self.definitions : ASN1SchemaDefinitions = None
        self.assignment_list : ASN1SchemaAssignmentList = None

    def prettyprint(self, out : TextIO):
        self.module_identifier.prettyprint(out)
        out.write('\n')
        for definition in self.definitions:
            definition.prettyprint(out)
            out.write('\n')
        self.assignment_list.prettyprint(out)
        out.write('\n')

class ASN1SchemaDefinitions (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()
        self.encoding_default : ASN1SchemaValue = None
        self.tag_default : ASN1SchemaValue = None
        self.extension_default : ASN1SchemaValue = None
        
class ASN1SchemaValue (ASN1SchemaRoot):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def prettyprint(self, out: TextIO):
        out.write(f'{{value : {self.value}}}')

class ASN1SchemaAssignmentList (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()
        self.type_assignments = List[ASN1SchemaAssignment]
        self.value_assignments = List[ASN1SchemaAssignment]

class ASN1SchemaAssignment (ASN1SchemaRoot):
    def __init__(self) -> None:
        super().__init__()

