""" swap table and function for rotating chars 180 degrees.
"""

swapTable = {
    '(':')',
    ')':'(',
    '.':'`',
    '`':'.',
    '_':'^',
    "'":','
    }

def rotate(char):
    """ Rotate char if it has a "symmetric" char. 
    """
    if char in swapTable.keys():
        return swapTable[char]
    else:
        return char
