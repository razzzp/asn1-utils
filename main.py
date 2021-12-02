from os import error

class ASN1Object:
    def __init__(self, type : str, value = None) -> None:
        super().__init__()
        self.isOptional = True
        self.type = type
        self.value = value

    def __str__(self) -> str:
        result = f'{{\ntype : {self.type}\nvalue : {self.value}\n}}'
        return result
    
class ASN1Sequence (ASN1Object):
    def __init__(self, type : str, value = None) -> None:
        super().__init__(type, value)
        self.children = []

    def __str__(self) -> str:
        result = f'{{\ntype : {self.type}\n'
        for obj in self.children:
            result += str(obj)
        result += '\n}'
        return result

class DERBooleanParser:
    #expected tag value
    Tag = 1

    def parse(self, length: int, value : bytes):
        if length > 1:
            raise ValueError("boolean cannot have length > 1")
        return ASN1Object('bool', bool(value[0]))

class DERIntegerParser:
    Tag = 2

    def parse(self, length: int, value : bytes):
        return ASN1Object('int', int.from_bytes(value,'big'))

#-----------

def getDataParser(tag):
    print(f'tag: {tag}')
    if tag == 1:
        return DERBooleanParser()
    if tag == 2:
        return DERIntegerParser()
    raise ValueError("tag not supported: " + str(tag))

def parseRecursive(data, underObject):
    length = len(data)
    curPos = 0
    generatedObjects = []
    while curPos < length:
        lengthPos = curPos+1
        valuePos = lengthPos+1
        #
        parser = getDataParser(data[curPos])
        print(f'parser: {type(parser)}')
        # get length for current tlv
        valueLength = data[lengthPos]
        # if first bit is one actual is in the next few bytes
        #print(str(valueLength&0x80))
        if (valueLength & 0x80):
            print("extended length")
            lengthPos +=1
            # length of length specified by bit 1-7
            lengthOfLength = valueLength & 0x7F
            lengthBytes = data[lengthPos:lengthPos+lengthOfLength]
            valueLength = int.from_bytes(lengthBytes, 'big')
            # set start of values
            valuePos = lengthPos + lengthOfLength

        # curPos updated to next TLV tag
        curPos = valuePos+valueLength
        valueBytes = data[valuePos : curPos]
        if parser:
            underObject.children.append(parser.parse(valueLength, valueBytes))
        else:
            parseRecursive(data, underObject)
        print(f'value: {valueBytes.hex()}')
        

    pass

def main():
    print("DER decoder")
    testBytes = bytes([1,1,1,2,0x81,4,0,0,0,255])
    rootNode = ASN1Sequence('root')
    parseRecursive(testBytes, rootNode)
    print(f'final result:\n {rootNode}')


if __name__ == "__main__":
    main()