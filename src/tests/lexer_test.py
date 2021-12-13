import sys, os
sys.path.append(os.path.join(os.getcwd(),'src'))

from asn1.parsers import ASN1Parser
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
    maxUInt8 INTEGER ::=255
    UInt8 ::= INTEGER (0..maxUInt8)
    maxUInt15 INTEGER ::= 32767
    UInt15 ::= INTEGER (0..maxUInt15)
    maxUInt16 INTEGER ::= 65535
    UInt16 ::= INTEGER (0..maxUInt16)
    maxUInt31 INTEGER ::= 2147483647
    UInt31 ::= INTEGER (0..maxUInt31)

    ApplicationIdentifier ::= OCTET STRING (SIZE(5..16))

    PEHeader ::= SEQUENCE {
    mandated NULL OPTIONAL,
    -- if set, indicate that the support of this PE is mandatory
    identification UInt15 -- Identification number of this PE
    }

    ProfileElement ::= CHOICE {
	header ProfileHeader,

/* PEs */
	genericFileManagement PE-GenericFileManagement,
	pinCodes PE-PINCodes,
	pukCodes PE-PUKCodes,
	akaParameter PE-AKAParameter,
	cdmaParameter PE-CDMAParameter,
	securityDomain PE-SecurityDomain,
	rfm PE-RFM,
	application PE-Application,
	nonStandard PE-NonStandard,
	end PE-End,
	rfu1 PE-Dummy, -- this avoids renumbering of tag values
	rfu2 PE-Dummy, -- in case other non-file-system PEs are
	rfu3 PE-Dummy, -- added here in future versions
	rfu4 PE-Dummy,
	rfu5 PE-Dummy,

/* PEs related to file system creation using templates defined in this specification */	
	mf PE-MF,
	cd PE-CD,
	telecom PE-TELECOM,
	usim PE-USIM,
	opt-usim PE-OPT-USIM,
	isim PE-ISIM,
	opt-isim PE-OPT-ISIM,
	phonebook PE-PHONEBOOK,
	gsm-access PE-GSM-ACCESS,
	csim PE-CSIM,
	opt-csim PE-OPT-CSIM,
	eap PE-EAP,
	df-5gs PE-DF-5GS,
	df-saip PE-DF-SAIP,
...
}
    END
    """)

    keywords = StringIO("""
     ABSENT
ABSTRACT-SYNTAX
ALL
APPLICATION
AUTOMATIC
BEGIN
BIT
BMPString
BOOLEAN
BY
CHARACTER
CHOICE
CLASS
COMPONENT
COMPONENTS
CONSTRAINED
CONTAINING
DATE
DATE-TIME
DEFAULT
DEFINITIONS
DURATION
EMBEDDED
ENCODED
ENCODING-CONTROL
END
ENUMERATED
EXCEPT
EXPLICIT
EXPORTS
EXTENSIBILITY
EXTERNAL
FALSE
FROM
GeneralizedTime
GeneralString
GraphicString
IA5String
IDENTIFIER
IMPLICIT
IMPLIED
IMPORTS
INCLUDES
INSTANCE
INSTRUCTIONS
INTEGER
INTERSECTION
ISO646String
MAX
MIN
MINUS-INFINITY
NOT-A-NUMBER
NULL
NumericString
OBJECT
ObjectDescriptor
OCTET
OF
OID-IRI
OPTIONAL
PATTERN
PDV
PLUS-INFINITY
PRESENT
PrintableString
PRIVATE
REAL
RELATIVE-OID
RELATIVE-OID-IRI
SEQUENCE
SET
SETTINGS
SIZE
STRING
SYNTAX
T61String
TAGS
TeletexString
TIME
TIME-OF-DAY
TRUE
TYPE-IDENTIFIER
UNION
UNIQUE
UNIVERSAL
UniversalString
UTCTime
UTF8String
VideotexString
VisibleString
WITH
    """)
    #print('out:\n')
    lexer = lexers.ASN1Lexer()

    lexemes = lexer._get_lexemes_v2(istream)

    with open('./out/test_lexemes.txt','w') as f:
        for lexeme in lexemes:
            f.write(lexeme + '\n')

    tokens = lexer._get_tokens(lexemes)
    
    with open('./out/test_tokens.txt','w') as f:
        for token in tokens:
            token.pretty_print(f)

    asn1schema = ASN1Parser().parse(tokens)

    with open('./out/test_schema.txt', 'w') as f:
        asn1schema.prettyprint(f)


