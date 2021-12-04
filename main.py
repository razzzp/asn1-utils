from os import error
import struct
from typing import ContextManager, List, Tuple

class ASN1Root:
    def __init__(self, type : str) -> None:
        self.type = type
        self.isOptional = True

    def asASN1Str(self) -> str:
        # to be overriden
        raise NotImplementedError(f'asASN1Str() is not implemented in {self.__class__}')

    @staticmethod
    def indentStr(indent):
        result = ''
        for i in range (indent):
            result +='\t'
        return result


class ASN1Object (ASN1Root):
    def __init__(self, type : str, value = None) -> None:
        super().__init__(type)
        self.value = value

    def asASN1Str(self, indent = 0) -> str:
        return f'{self.indentStr(indent)}{self.type} ::= {self.value}'
    
class ASN1Sequence (ASN1Root):
    def __init__(self) -> None:
        super().__init__('sequence')
        self.children : List[ASN1Root] = []

    def asASN1Str(self, indent = 0) -> str:
        result = f'{self.indentStr(indent)}{self.type} :: = {{\n'
        for child in self.children:
            result += child.asASN1Str(indent+1) + '\n'
        result += self.indentStr(indent) + '}'
        return result

class DERBooleanDecoder:
    #expected tag value
    TagNum = 1 #0x01

    @staticmethod
    def decode(length: int, value : bytes):
        if length > 1:
            raise ValueError("boolean cannot have length > 1")
        # TODO in DER True has to be 0xFF
        return ASN1Object('bool', bool(value[0]))


class DERIntegerDecoder:
    TagNum = 2 #0x02

    @staticmethod
    def decode(length: int, value : bytes):
        return ASN1Object('int', int.from_bytes(value,'big'))

class DEREnumDecoder (DERIntegerDecoder):
    TagNum = 10 #0x0A

class DERRealValueDecoder:
    TagNum = 9 #0x09

    @staticmethod
    def decode(length : int, value : bytes):
        [num] =struct.unpack('f',value)
        return ASN1Object('real', num)

class DERBitStringDecoder:
    TagNum = 3 #0x03

    @staticmethod
    def decode(length : int,value : bytes):
        raise NotImplementedError(f'{__name__} is not implemented')
        # TODO

class DEROctetStringDecoder:
    TagNum = 4 #0x04

    @staticmethod
    def decode(length : int, value : bytes):
        [strVal] = struct.unpack(f'{len(value)}s', value)
        return ASN1Object('octet string', str(strVal, 'utf-8'))

class DERNullDecoder:
    TagNum = 5 #0x05

    @staticmethod
    def decode(length : int,value : bytes):
        return ASN1Object('null')

class DERObjectIdentifierDecoder:
    TagNum = 6 #0x06

    @staticmethod
    def decode(length : int, value : bytes):
        pass

class DERSequenceDecoder:
    # class - universal
    # type - constructed 
    TagNum = 16 #0x10

    def __init__(self) -> None:
        self.value = None

    def decode(self, length: int, value : bytes):
        self.value = value
        curPos = 0
        result = ASN1Sequence()
        
        while curPos < length:
            # reset loop vars
            tagClass = tagType = tagNumber = 0
            valLength = 0
            valueBytes = None
            decoder = None

            # byte at curpos is the tag
            (tagClass, tagType, tagNumber, curPos) = self._readTag(curPos)

            # get decoder for tag
            try:
                decoder = getDERDataDecoder(tagClass, tagType, tagNumber)
            except ValueError as e:
                print(f'Warning: {e}. Block will be skipped')

            print(f'parser: {type(decoder)}')

            # get length for current tlv
            (valLength, curPos) = self._readLength(curPos)

            # get values
            if valLength:
                (valueBytes, curPos) = self._readValue(curPos, valLength)
                print(f'value: {valueBytes.hex()}')

            if decoder:
                #decode value bytes and append to children
                result.children.append(decoder.decode(valLength, valueBytes))
        #
        return result

    def _readTag(self, index : int) -> tuple:
        """Reads byte at @index in self.value, and determine the tag of the TLV.
            Tag can be of the extended type
        """
        try:
            tag = self.value[index]
        except error:
            raise IndexError(error)
        # bits 8-7
        tagClass = tag & 0xc0
        # bit 6
        tagType = tag & 0x20
        
        #check if extended (bit 5-1 all '1')
        if tag & 0x1f == 0x1f:
            #raise ValueError('extended tags not supported')
            tagNum = 0
            isLastbyte = False
            while(not isLastbyte):
                index += 1
                curByte = self.value[index]
                tagNum = (tagNum << 7) | curByte & 0x7f
                isLastbyte = curByte & 0x80 != 0x80
        else:
            tagNum = tag & 0x1f
            
        nextIndex = index + 1
        return (tagClass, tagType, tagNum, nextIndex)

    def _readLength(self, index : int) -> tuple:
        """Reads the byte at @index, and determine the length of the TLV.
            Length can be the extended type
        """
        try:
            curByte = self.value[index]
        except error:
            raise IndexError(error)
        curByte = self.value[index]
        #checks if extended length
        if (curByte & 0x80):
            #print("extended length")
            # length of length specified by bit 1-7
            lengthOfLength = curByte & 0x7F
            index +=1
            lengthBytes = self.value[index:index+lengthOfLength]
            length = int.from_bytes(lengthBytes, 'big')
            # set start position of values bytes
            nextIndex = index + + lengthOfLength
        else:
            length = curByte
            nextIndex = index + 1
        
        return (length, nextIndex)

    def _readValue(self, index : int, length : int) -> tuple:
        """Reads from self.value starting from @index for @length bytes"""
        try:
            t = self.value[index]
        except error:
            raise IndexError(error)
        nextIndex = index + length
        value = self.value[index : nextIndex]
        return (value, nextIndex)

# enums ----------

# Tag structure
#   |b8 |b7 |b6  |b5 |b4 |b3 |b2 |b1 |
#   |class  |type|number             |
class TagClass:
    Universal = 0x00
    Application = 0x40
    Context_Specific = 0x80
    Private = 0xc0

class TagType:
    Primitive = 0x00
    Constructed = 0x20


# global -----------

def main():
    print("ASN1 Utils - DER Decoder")
    #
    testBytes = getTestData()
    #
    parser = DERSequenceDecoder()
    result = parser.decode(len(testBytes), testBytes)
    print(f'\nfinal result:')
    #
    print(result.asASN1Str())

def getDERDataDecoder(tagClass, tagType, tagNum):
    print(f'cla: {tagClass}; type: {tagType}; num: {tagNum}')
    if tagClass == TagClass.Universal:
        if tagType == TagType.Primitive:
           return primitiveDecoderMapping[tagNum]
        elif tagType == TagType.Constructed:
            if tagNum == DERSequenceDecoder.TagNum:
                return DERSequenceDecoder()
    raise ValueError(f'tag not supported: cla: {tagClass}; type: {tagType}; num: {tagNum}')

primitiveDecoderMapping = {
    DERBooleanDecoder.TagNum : DERBooleanDecoder(),
    DERIntegerDecoder.TagNum : DERIntegerDecoder(),
    DEREnumDecoder.TagNum : DEREnumDecoder(),
    DERRealValueDecoder.TagNum : DERRealValueDecoder(),
    DERBitStringDecoder.TagNum : DERBitStringDecoder(),
    DEROctetStringDecoder.TagNum : DEROctetStringDecoder(),
    DERNullDecoder.TagNum : DERNullDecoder(),
    DERObjectIdentifierDecoder.TagNum : DERObjectIdentifierDecoder()
}

def getTestData() -> bytes:
    # bool
    result = b'\x01\x01\x01'
    # int
    result += b'\x02\x01\x10'
    # ex int
    result += b'\x02\x81\x04\x80\x00\x00\xee'
    # unsupported class
    result += b'\xff\x8f\x01\x00'
    # bool 
    result += b'\x01\x01\xff'
    # octet string
    result += b'\x04\x0bhello world'
    # sequence with primitives
    result += b'\x30\x0b\x01\x01\xff\x02\x01\x20\x02\x81\x02\x01\x00'
    return result

if __name__ == "__main__":
    main()
