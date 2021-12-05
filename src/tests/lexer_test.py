import sys, os
sys.path.append(os.path.join(os.getcwd(),'src'))


from asn1 import lexers
from io import StringIO


def run():
    istream = StringIO("""
    PEDefinitions {joint-iso-itu-t(2) international-organizations(23) simalliance(143) euicc-profile(1) spec-version(1) version-two(2)}
    DEFINITIONS
    AUTOMATIC TAGS
    EXTENSIBILITY IMPLIED ::=
    BEGIN

    -- Basic integer types, for size constraints
    maxUInt8 INTEGER ::= 255
    UInt8 ::= INTEGER (0..maxUInt8)
    maxUInt15 INTEGER ::= 32767
    UInt15 ::= INTEGER (0..maxUInt15)
    maxUInt16 INTEGER ::= 65535
    UInt16 ::= INTEGER (0..maxUInt16)
    maxUInt31 INTEGER ::= 2147483647
    UInt31 ::= INTEGER (0..maxUInt31)

    ApplicationIdentifier ::= OCTET STRING (SIZE(5..16))
    END
    """)
    print('out:\n')
    lexer = lexers.ASN1Lexer()
    result = lexer.tokenize(istream)
    print(result)

