"""
Helper method generates one block size per time
Input: 1. python file object
       2. block size specified by user
Output: new block size of the file
"""


def read_in_chunks(file_object, block_size):
    while True:
        data = file_object.read(block_size)
        if not data:
            break
        yield data


"""
Method for reading the plaintext file
Input: 1. name of plaintext file
       2. block size 
Output: list of the plaintext broken up into the sizes specified by user
"""


def file_read(filename, block_size=64):
    list_of_chunks = []
    with open(filename) as f:
        for piece in read_in_chunks(f, block_size):
            list_of_chunks.append(piece)
            print(piece, len(piece.encode('utf-8')))
    return list_of_chunks


"""
RC4 Algorithm
"""

"""
Method for generating the RC4 S-box
Input: Secret key
Output: 256 * 256 matrix shuffled with the key
"""


def s_initialization(key):
    K = [ord(c) for c in key]  # Convert the key to bytes
    S = [i for i in range(256)]  # Initializing the S values (0 - 255)
    T = [K[i % len(K)] for i in range(256)]  # Building the T list

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]
    return S


"""
Helper Method that generates the next byte stream
Input: S-box
Output: next byte stream to be XORed
"""


def stream_generation(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        k = S[t]
        yield k


"""
Method that creates a generator that presents the next byte stream when called
Input: S-box 
Output: next byte stream to be XORed
"""


def key_stream(S):
    return stream_generation(S)


"""
Method for encrypting plaintext - i.e. XORing each character with the next key byte stream
Input: 1. symmetric key
       2. plaintext
Output: Cipher text 
"""


def encryption_rc4(key, plaintext):
    S = s_initialization(key)
    stream = key_stream(S)
    cipher = []
    for letter in plaintext:
        letter_byte = ord(letter)
        cipher_letter = letter_byte ^ stream.__next__()
        cipher.append(chr(cipher_letter))
    return ''.join(cipher)


"""
Method for decrypting the cipher text
Input: 1. symmetric key 
       2. cipher text
Output: plaintext 
"""


def decryption_rc4(key, ciphertext):
    S = s_initialization(key)
    stream = key_stream(S)
    plain = []
    for letter in ciphertext:
        letter_byte = ord(letter)
        plain_letter = letter_byte ^ stream.__next__()
        plain.append(chr(plain_letter))
    result = ''.join(plain)
    return result.replace('0', '')
