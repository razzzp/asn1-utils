from asn1.decoders import *

def main():
    print("ASN1 Utils - DER Decoder")
    #
    testBytes = getTestData()
    #
    parser = DERSequenceDecoder()
    result = parser.decode(len(testBytes), testBytes)
    print(f'\nfinal result:')
    #
    print(result.as_asn1_str())

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
    # nested sequence
    result += b'\x30\x10\x30\x0b\x01\x01\xff\x02\x01\x20\x02\x81\x02\x01\x00\x01\x01\xff'
    return result

if __name__ == "__main__":
    main()
