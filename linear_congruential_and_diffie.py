import random

"""
Method for generating user private keys. This key generation id based on Combined Linear congruential generator
Input: number of keys you want to create
Output: a list of the created keys
"""


def linear_congruential(number_of_random_numbers):
    private_keys = []
    m1 = 2147483646
    m2 = 2147483425
    a1 = 460
    a2 = 244
    y01 = 2147483645
    y02 = 2147483424
    for i in range(number_of_random_numbers):
        y1_rand = random.randint(1, y01)
        y2_rand = random.randint(1, y02)
        y1 = (a1 * y1_rand) % m1
        y2 = (a2 * y2_rand) % m2
        x = (y1 - y2) % (m1 - 1)
        if x > 0:
            x = x / m1
        if x == 0:
            x = (m1 - 1) / m1
        private_keys.append(x)
    print("******************** GENERATING PRIVATE KEYS FOR", number_of_random_numbers, "Users **********************")
    print("[LINEAR CONGRUENTIAL]", 'Private key for Alice:', private_keys[0])
    print("[LINEAR CONGRUENTIAL]", 'Private key for Bob:', private_keys[1])
    return private_keys


"""
Method for generating public and private key pair for each user using the Diffie hellman algorithm
Input: 1. q : a prime number
       2. alpha: a primitive root of q
       3. private keys 
Output: The symmetric key generated from the users' public = and private key
"""


def diffie_hellman(q, alpha, private_keys):
    # Generate private keys using combined linear congruential generator
    symmetric_key = 0
    # Generate public keys
    users = ["Alice", "Bob"]
    public_keys = []
    for key in private_keys:
        pub_key = (alpha ** key) % q
        public_keys.append(pub_key)
    print("********************* GENERATING KEY PAIRS FOR USERS USING DIFFIE HELLMAN *********************************")
    print("[DIFFIE HELLMAN]", "Key Pair for", users[0], "[ public key:", public_keys[0], 'private key:',
          private_keys[0], ']')
    print("[DIFFIE HELLMAN]", "Key Pair for", users[1], "[ public key:", public_keys[1], 'private key:',
          private_keys[1], ']')
    # Generate secret keys
    public_keys.reverse()
    for i, key in enumerate(public_keys):
        symmetric_key = (key ** private_keys[i]) % q
        print("[ Secret key for", users[i], "==============>", symmetric_key, ']')
    return str(symmetric_key)


"""
Method for encrypting the last 64 block of the text
Input: 1. name of the file containing the plaintext
       2. block size for breaking up the plaintext(e.g 8, 64, 128 bits)
       3. symmetric key known to sender and receiver
Output: a string representing the ciphertext

"""


def encryption(filename, block_size, secret_key):
    print('******************************** ENCRYPTING PLAINTEXT WITH RC4 ALGORITHM **********************************')
    plaintext_blocks = file_read(filename, block_size)
    encryption_block = plaintext_blocks.pop(len(plaintext_blocks) - 1)
    if len(encryption_block) < block_size:
        encryption_block = encryption_block.rjust(block_size, '0')
        print("length of encryption block after padding", len(encryption_block))
        print(encryption_block)
    print("[RC4 ENCRYPTION]", "Plaintext:", encryption_block)
    ciphertext = encryption_rc4(secret_key, encryption_block)
    print("[RC4 ENCRYPTION]", "Ciphertext:", ciphertext)
    return ciphertext


"""
Method for decrypting the ciphertext
Input: 1. symmetric key known to the user and receiver
       2. cipher text 
Output: plaintext
"""


def decryption(secret_key, ciphertext):
    print('******************************* DECRYPTING CIPHERTEXT WITH RC4 ALGORITHM **********************************')
    plaintext = decryption_rc4(secret_key, ciphertext)
    print("[RC4 DECRYPTION]", "Plaintext:", plaintext)
    return plaintext

if __name__ == '__main__':
    keys = linear_congruential(2)
    secret_key = diffie_hellman(253, 3, keys)
    ciphertext = encryption('file2.txt', 64, secret_key)
    plaintext = decryption(secret_key, ciphertext)
