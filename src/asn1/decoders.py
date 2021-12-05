from os import error
from asn1 import *
import struct

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

# decoder classes ----

class DERBooleanDecoder:
    #expected tag value
    TAG_NUM = 1 #0x01

    @staticmethod
    def decode(length: int, value : bytes):
        if length > 1:
            raise ValueError("boolean cannot have length > 1")
        # TODO in DER True has to be 0xFF
        return ASN1Object('bool', bool(value[0]))


class DERIntegerDecoder:
    TAG_NUM = 2 #0x02

    @staticmethod
    def decode(length: int, value : bytes):
        return ASN1Object('int', int.from_bytes(value,'big'))

class DEREnumDecoder (DERIntegerDecoder):
    TAG_NUM = 10 #0x0A

class DERRealValueDecoder:
    TAG_NUM = 9 #0x09

    @staticmethod
    def decode(length : int, value : bytes):
        [num] =struct.unpack('f',value)
        return ASN1Object('real', num)

class DERBitStringDecoder:
    TAG_NUM = 3 #0x03

    @staticmethod
    def decode(length : int,value : bytes):
        raise NotImplementedError(f'{__name__} is not implemented')
        # TODO

class DEROctetStringDecoder:
    TAG_NUM = 4 #0x04

    @staticmethod
    def decode(length : int, value : bytes):
        [strVal] = struct.unpack(f'{len(value)}s', value)
        return ASN1Object('octet string', str(strVal, 'utf-8'))

class DERNullDecoder:
    TAG_NUM = 5 #0x05

    @staticmethod
    def decode(length : int,value : bytes):
        return ASN1Object('null')

class DERObjectIdentifierDecoder:
    TAG_NUM = 6 #0x06

    @staticmethod
    def decode(length : int, value : bytes):
        pass

class DERSequenceDecoder:
    # class - universal
    # type - constructed 
    TAG_NUM = 16 #0x10

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
            (tagClass, tagType, tagNumber, curPos) = self._read_tag(curPos)

            # get decoder for tag
            try:
                decoder = get_der_decoder(tagClass, tagType, tagNumber)
            except ValueError as e:
                print(f'Warning: {e}. Block will be skipped')

            print(f'parser: {type(decoder)}')

            # get length for current tlv
            (valLength, curPos) = self._read_length(curPos)

            # get values
            if valLength:
                (valueBytes, curPos) = self._read_value(curPos, valLength)
                print(f'value: {valueBytes.hex()}')

            if decoder:
                #decode value bytes and append to children
                result.children.append(decoder.decode(valLength, valueBytes))
        #
        return result

    def _read_tag(self, index : int) -> tuple:
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

    def _read_length(self, index : int) -> tuple:
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

    def _read_value(self, index : int, length : int) -> tuple:
        """Reads from self.value starting from @index for @length bytes"""
        try:
            t = self.value[index]
        except error:
            raise IndexError(error)
        nextIndex = index + length
        value = self.value[index : nextIndex]
        return (value, nextIndex)


# static maps
_primitiveDecoderMapping = {
    DERBooleanDecoder.TAG_NUM : DERBooleanDecoder(),
    DERIntegerDecoder.TAG_NUM : DERIntegerDecoder(),
    DEREnumDecoder.TAG_NUM : DEREnumDecoder(),
    DERRealValueDecoder.TAG_NUM : DERRealValueDecoder(),
    DERBitStringDecoder.TAG_NUM : DERBitStringDecoder(),
    DEROctetStringDecoder.TAG_NUM : DEROctetStringDecoder(),
    DERNullDecoder.TAG_NUM : DERNullDecoder(),
    DERObjectIdentifierDecoder.TAG_NUM : DERObjectIdentifierDecoder()
}

def get_der_decoder(tagClass, tagType, tagNum):
    print(f'cla: {tagClass}; type: {tagType}; num: {tagNum}')
    if tagClass == TagClass.Universal:
        if tagType == TagType.Primitive:
           return _primitiveDecoderMapping[tagNum]
        elif tagType == TagType.Constructed:
            if tagNum == DERSequenceDecoder.TAG_NUM:
                return DERSequenceDecoder()
    raise ValueError(f'tag not supported: cla: {tagClass}; type: {tagType}; num: {tagNum}')