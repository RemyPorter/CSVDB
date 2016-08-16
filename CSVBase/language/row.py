"""
A specialized definition of a CSV language, specifically for
handling my unique cases.

>>> quotedField.parseString(test_quote)
(['Some, quoted, fields'], {})
>>> row.parseString(test_row)
(['One', 'Two', 'Three, values'], {})
>>> row.parseString('1!')
(['1'], {})
"""
from pyparsing import *
delimiter = Suppress(",")
bareField = CharsNotIn(",\n\"!")
pairedQuotes = Suppress("''").setParseAction(lambda x: '"')
quotedField = Suppress('"') + (CharsNotIn('"') | pairedQuotes) + Suppress('"')
field = (quotedField | bareField)
field.setParseAction(lambda s: s[0].strip())
rowDelimiter = Suppress("!")
row = field + ZeroOrMore(delimiter + field) + rowDelimiter

if __name__ == '__main__':
    import doctest
    test_quote = "\"Some, quoted, fields\""
    test_row = 'One, Two, "Three, values"!'
    doctest.testmod()