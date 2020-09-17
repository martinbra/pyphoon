""" swap table and function for rotating chars 180 degrees.
"""

SWAP_TABLE = {
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
    if char in SWAP_TABLE.keys():
        return SWAP_TABLE[char]

    return char
