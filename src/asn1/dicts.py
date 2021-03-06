MultiCharSymbol = {
    '.' : 'dot',
    ':' : 'colon',
    '[' : 'start_square_brace',
    ']' : 'end_square_brace',
    '*' : 'asterik',
    '/' : 'forward_slash',
    '-' : 'hypen'
    # </ and /> not supported
}

MultiCharSymbolLexemes ={
    '..' : 'double_dot',
    '....' : 'triple_dot',
    '[[' : 'double_start_square_brace',
    ']]' : 'double_end_square_brace',
    '/*' : 'start comment',
    '*/' : 'end_comment',
    '--' : 'single line comment',
    '::=' : 'assignment'
}

SingleCharSymbol = {
    '=' : 'equals',
    '\'' : 'quote',
    '\"' : 'double_quotes',
    ',' : 'comma',
    # hypens can be in identifiers
    #'-' : 'hypen',
    #'/' : 'slash',
    #':' : 'colon',
    ';' : 'semi_colon',
    '@' : 'at',
    '|' : 'pipe',
    '!' : 'exclamation',
    '^' : 'caret',
     '(' : 'start_brace',
    '{' : 'start_curly_brace',
    #'[' : 'start_square_brace',
    '<' : 'less_than',
     ')' : 'end_brace',
    '}' : 'end_curly_brace',
    #']' : 'end_square_brace',
    '>' : 'greater_than',
}

WhiteSpace = {
    ' ' : 'space',
    '\n' : 'newline',
    '\t' : 'tab'
}

Keywords = {
    'ABSENT',
    'ABSTRACT-SYNTAX',
    'ALL',
    'APPLICATION',
    'AUTOMATIC',
    'BEGIN',
    'BIT',
    'BMPString',
    'BOOLEAN',
    'BY',
    'CHARACTER',
    'CHOICE',
    'CLASS',
    'COMPONENT',
    'COMPONENTS',
    'CONSTRAINED',
    'CONTAINING',
    'DATE',
    'DATE-TIME',
    'DEFAULT',
    'DEFINITIONS',
    'DURATION',
    'EMBEDDED',
    'ENCODED',
    'ENCODING-CONTROL',
    'END',
    'ENUMERATED',
    'EXCEPT',
    'EXPLICIT',
    'EXPORTS',
    'EXTENSIBILITY',
    'EXTERNAL',
    'FALSE',
    'FROM',
    'GeneralizedTime',
    'GeneralString',
    'GraphicString',
    'IA5String',
    'IDENTIFIER',
    'IMPLICIT',
    'IMPLIED',
    'IMPORTS',
    'INCLUDES',
    'INSTANCE',
    'INSTRUCTIONS',
    'INTEGER',
    'INTERSECTION',
    'ISO646String',
    'MAX',
    'MIN',
    'MINUS-INFINITY',
    'NOT-A-NUMBER',
    'NULL',
    'NumericString',
    'OBJECT',
    'ObjectDescriptor',
    'OCTET',
    'OF',
    'OID-IRI',
    'OPTIONAL',
    'PATTERN',
    'PDV',
    'PLUS-INFINITY',
    'PRESENT',
    'PrintableString',
    'PRIVATE',
    'REAL',
    'RELATIVE-OID',
    'RELATIVE-OID-IRI',
    'SEQUENCE',
    'SET',
    'SETTINGS',
    'SIZE',
    'STRING',
    'SYNTAX',
    'T61String',
    'TAGS',
    'TeletexString',
    'TIME',
    'TIME-OF-DAY',
    'TRUE',
    'TYPE-IDENTIFIER',
    'UNION',
    'UNIQUE',
    'UNIVERSAL',
    'UniversalString',
    'UTCTime',
    'UTF8String',
    'VideotexString',
    'VisibleString',
    'WITH',   
}

Separators = {
     ',',
     '(',
     '[',
     '{',
     ')',
     ']',
     '}',
     ';'
}

Operators = {
    '=',
    '+',
    '|',
    '!',
    '<',
    '>',
    '@',
    '.',
    '*',
    '^',
    '::='
}