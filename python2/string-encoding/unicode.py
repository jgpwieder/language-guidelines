from utils import printVal, printRepresentations


content = "cafe"
byteContent = "\x63\x61\x66\x65"  # You can define a string by passing its bytes

printVal(content)
printVal(byteContent)
# There is no difference between the two ways of defining a string

print("\nSimple ASC string")
printRepresentations(content)

print("\nUnicode string only with asc characters")
content = u'cafe'
printRepresentations(content)
