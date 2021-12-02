from os import error
import struct
from typing import ContextManager, Tuple

class ASN1Root:
    def __init__(self, type : str) -> None:
        self.type = type
        self.isOptional = True

class ASN1Object (ASN1Root):
    def __init__(self, type : str, value = None) -> None:
        super().__init__(type)
        self.value = value

    def __str__(self) -> str:
        result = f'{{\ntype : {self.type}\nvalue : {self.value}\n}}'
        return result
    
class ASN1Sequence (ASN1Root):
    def __init__(self, type : str) -> None:
        super().__init__(type)
        self.children = []

    def __str__(self) -> str:
        result = f'{{\ntype : {self.type}\nchildren : \n'
        for obj in self.children:
            result += str(obj) + '\n'
        result += '\n}'
        return result

class DERBooleanDecoder:
    #expected tag value
    Tag = 1 #0x01

    @staticmethod
    def decode(length: int, value : bytes):
        if length > 1:
            raise ValueError("boolean cannot have length > 1")
        # TODO in DER True has to be 0xFF
        return ASN1Object('bool', bool(value[0]))


class DERIntegerDecoder:
    Tag = 2 #0x02

    @staticmethod
    def decode(length: int, value : bytes):
        return ASN1Object('int', int.from_bytes(value,'big'))

class DERRealValueDecoder:
    Tag = 9 #0x09

    @staticmethod
    def decode(length : int, value : bytes):
        [num] =struct.unpack('f',value)
        return ASN1Object('real', num)

class DERBitStringDecoder:
    Tag = 3 #0x03

    @staticmethod
    def decode(length : int,value : bytes):
        raise NotImplementedError(f'{__name__} is not implemented')
        # TODO

class DEROctetStringDecoder:
    Tag = 4 #0x04

    @staticmethod
    def decode(length : int,value : bytes):
        [strVal] = struct.unpack('s', value)
        return ASN1Object('octet string', strVal)

class DERNullDecoder:
    Tag = 5 #0x30

    @staticmethod
    def decode(length : int,value : bytes):
        return ASN1Object('null')

class DERSequenceDecoder:
    Tag = 48 #0x30

    def __init__(self) -> None:
        self.value = None

    def decode(self, length: int, value : bytes):
        self.value = value
        result = []
        curPos = 0
        
        while curPos < length:
            # byte at curpos is the tag
            (tagClass, tagType, tagNumber, curPos) = self._readTag(curPos)

            # get decoder for tag
            decoder = getDERDataDecoder(tagClass, tagType, tagNumber)
            print(f'parser: {type(decoder)}')

            # get length for current tlv
            (valLength, curPos) = self._readLength(curPos)

            # get values
            (valueBytes, curPos) = self._readValue(curPos, valLength)

            if decoder:
                #decode value bytes and append to children
                result.append(decoder.decode(valLength, valueBytes))
            print(f'value: {valueBytes.hex()}')

        #
        return result

    def _readTag(self, index : int) -> tuple:
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
            tagNum = tag
            
        nextIndex = index + 1
        return (tagClass, tagType, tagNum, nextIndex)

    def _readLength(self, index : int) -> tuple:
        try:
            curByte = self.value[index]
        except error:
            raise IndexError(error)
        curByte = self.value[index]
        if (curByte & 0x80):
            print("extended length")
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
        try:
            t = self.value[index]
        except error:
            raise IndexError(error)
        nextIndex = index + length
        value = self.value[index : nextIndex]
        return (value, nextIndex)

# enums ----------

class TagClass:
    Universal = 0x00
    Application = 0x01
    Context_Specific = 0x10
    Private = 0x11

class TagType:
    Primitive = 0x00
    Constructed = 0x20


# global -----------

def getDERDataDecoder(tagClass, tagType, tagNum):
    print(f'cla: {tagClass}; type: {tagType}; num: {tagNum}')
    if tagClass == TagClass.Universal:
        if tagType == TagType.Primitive:
            if tagNum == DERBooleanDecoder.Tag:
                return DERBooleanDecoder()
            if tagNum == DERIntegerDecoder.Tag:
                return DERIntegerDecoder()  
        elif tagType == TagType.Constructed:
            if tagNum == DERSequenceDecoder.Tag:
                return DERSequenceDecoder() 
    raise ValueError(f'tag not supported: cla: {tagClass}; type: {tagType}; num: {tagNum}')

def main():
    print("DER decoder")
    testBytes = bytes(b'\x01\x01\x01\x02\x81\x04\x00\x00\x00\xee\xff\x8f\x01\x00')
    parser = DERSequenceDecoder()
    result = parser.decode(len(testBytes), testBytes)
    print(f'final result:')
    for obj in result:
        print(f'\n{obj}')
    


if __name__ == "__main__":
    main()