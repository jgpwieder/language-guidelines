# coding=utf-8
# declares the encoding used for the source code in file so comments don't break
from utils import printRepresentations
from testStrings import accentuatedContent, accentuatedUnicodeContent

print("\nNot ASC unicode string")
content = accentuatedContent
unicodeContent = accentuatedUnicodeContent
byteContent = "\x63\x61\x66\xc3\xa9"  # cafe with accentuation

print("\n-content: ")
printRepresentations(content)

print("\n-unicodeContent: ")
printRepresentations(unicodeContent)

print("\n-byteContent: ")
printRepresentations(byteContent)

# -content:
# type = 'str'     , value = café
# type = 'list'    , value = [99, 97, 102, 195, 169]              NOTE: When ASCII represents a Not ASCII it uses escaping with 2 bytes
# type = 'list'    , value = ['63', '61', '66', 'c3', 'a9']             from the extended ASCII Codes é = ASCII(195) + ASCII(169)
# type = 'str'     , value = \x63\x61\x66\xc3\xa9
# type = 'str'     , value = café
#
# -unicodeContent:
# type = 'str'     , value = ENCODED-> café <-ENCODED             NOTE: To print a unicode character that is not ASCII need to encode to utf8
# type = 'list'    , value = [99, 97, 102, 233]                   NOTE: 233 is defined in the UNICODE and is é
# type = 'list'    , value = ['63', '61', '66', 'e9']
# type = 'str'     , value = \x63\x61\x66\xe9
# type = 'str'     , value = caf�                                 NOTE: This is expected not to work since 233 is not valid in ASC table
#                                                                        and no instruction was given that it is unicode
# -byteContent:
# type = 'str'     , value = café
# type = 'list'    , value = [99, 97, 102, 195, 169]
# type = 'list'    , value = ['63', '61', '66', 'c3', 'a9']
# type = 'str'     , value = \x63\x61\x66\xc3\xa9
# type = 'str'     , value = café


# Byte Strings (str):
# These are raw bytes. The character 'é' can be represented in different ways in bytes depending on the encoding used.
# For example, in Latin-1 (ISO-8859-1) encoding, 'é' is a single byte \xe9. However, in UTF-8 encoding, 'é' is
# represented by two bytes: \xc3\xa9.
# When Python 2 reads a byte string, it doesn't interpret the encoding unless you explicitly decode it to
# a unicode object. It simply sees str as a sequence of bytes and when you print a str object containing 'é',
# it sends those bytes directly to the output, which may render as 'é' or something else depending on the
# output device's encoding settings.
#
# Unicode Strings (unicode):
# A unicode object in Python 2 represents a sequence of Unicode code points. The character 'é' in a unicode object
# is represented internally by Python as the code point U+00E9. This code point corresponds to the decimal number 233.
# When you work with unicode objects and print them, Python 2 will attempt to encode them to the default system
# encoding (which is often ASCII, but can be set to something else) before sending the characters to the output.
# If the default encoding cannot represent the character, Python will raise a UnicodeEncodeError unless the unicode
# string is explicitly encoded to a byte string using an encoding that can represent the character.
#
# CONCLUSION:
# So when you pass 'é' as a byte string (not unicode), Python 2 interprets it directly as bytes, which can look
# different depending on the encoding of those bytes. When you pass 'é' as a unicode string, Python 2 uses the
# Unicode code point for that character, which is a consistent integer value (233 in the case of 'é') regardless
# of the encoding.
