"""
A specialized definition of a CSV language, specifically for
handling my unique cases.

>>> quotedField.parseString(test_quote)
(['Some, quoted, fields'], {})
>>> row.parseString(test_row)
(['One', 'Two', 'Three, values'], {})
>>> row.parseString('1')
(['1'], {})
"""
from pyparsing import *
quotedField = QuotedString('"').setParseAction(lambda t: t[0].replace("''", '"'))
list_item = quotedField | Word(printables, excludeChars=',')
row = delimitedList(list_item)

if __name__ == '__main__':
    import doctest
    test_quote = "\"Some, quoted, fields\""
    test_row = 'One, Two, "Three, values"'
    doctest.testmod()