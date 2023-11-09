from gzip import GzipFile
from StringIO import StringIO


def _readAndParseGzip(filename):
    file = open(filename, 'rb')
    content = file.read()
    unzipped = GzipFile(fileobj=StringIO(content)).read()
    return unzipped


def integerToHex(val):
    return "{:02x}".format(val)


def charToHex(val):
    return "{:02x}".format(ord(val))


def stringToIntegers(val):
    return [ord(char) for char in val]  # ord returns the unicode integer representation of each char


def stringToHex(val):
    return [charToHex(char) for char in val]


def stringToEscapedHex(val):
    return ''.join('\\x{}'.format(charToHex(char)) for char in val)


def escapedHexToString(val):
    return val.decode('string_escape')


def printVal(val):
    if isinstance(val, unicode) and not isAscii(val):
        val = "ENCODED-> " + val.encode('utf-8') + " <-ENCODED"

    print("type: {type}, value: {value}".format(
        value=val,
        type=str(type(val)).ljust(17),
    ))


def printRepresentations(val):
    printVal(val)
    printVal(stringToIntegers(val))

    printVal(stringToHex(val))

    byteRepresentation = stringToEscapedHex(val)
    printVal(byteRepresentation)
    printVal(escapedHexToString(byteRepresentation))


def stringInstance(val):  # No difference from printing the type
    if isinstance(val, unicode):
        return "unicode"
    if isinstance(val, str):
        return "byte string"
    return "not string"


def isAscii(val):
    try:
        val.decode('ascii')
        return True
    except:
        return False
