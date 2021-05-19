import string

"""
This function takes a string key value and constructs the the key lookup table for encryption and decryption
"""


def construct_lookup_table(key):
    key_table_list = []
    for character in key.upper():
        if character not in key_table_list:
            key_table_list.append(character)

    alphabet_string = string.ascii_uppercase
    alphabet_list = list(alphabet_string)
    for character in alphabet_list:
        if character not in key_table_list:
            key_table_list.append(character)
    key_table_list.remove('J')  # Removing the letter J since per play fair algorithm for key table construction

    # Construct 5*5 matrix table from the key table list
    key_table_five_by_five = [['' for i in range(5)] for j in range(5)]
    key_table_five_by_five[0] = key_table_list[0:5]
    key_table_five_by_five[1] = key_table_list[5:10]
    key_table_five_by_five[2] = key_table_list[10:15]
    key_table_five_by_five[3] = key_table_list[15:20]
    key_table_five_by_five[4] = key_table_list[20:25]
    return key_table_five_by_five


"""
This function returns the position(row, column) given the key table matrix and the letter
"""


def find_position(letter, key_table):
    for row in range(len(key_table)):
        for col in range(len(key_table[row])):
            if key_table[row][col] == letter:
                return row, col


"""
This function implements the encryption rules given two letters and the key table.
The rules are:
1. If both letters are in the same row take the letter to the right of each(going back to the left if at 
furthest right)
2. If the letters are in the same column takes the letters below each(going back to the top if at the bottom)
3. If neither of the preceding are true, form a rectangle with the two letters an take the letters on the horizontal
opposite corner of the rectangle
"""


def calculate_position_to_encrypt(letter1, letter2, key_table):
    row1, col1 = find_position(letter1, key_table)
    row2, col2 = find_position(letter2, key_table)
    if row1 == row2:
        return key_table[row1][(col1 + 1) % 5] + key_table[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return key_table[(row1 + 1) % 5][col1] + key_table[(row2 + 1) % 5][col2]
    else:
        return key_table[row1][col2] + key_table[row2][col1]


"""
This function implements the rules of decryption(the encryption rules applied in reverse)
"""


def calculate_position_to_decrypt(letter1, letter2, key_table):
    row1, col1 = find_position(letter1, key_table)
    row2, col2 = find_position(letter2, key_table)
    if row1 == row2:
        return key_table[row1][(col1 - 1) % 5] + key_table[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return key_table[(row1 - 1) % 5][col1] + key_table[(row2 - 1) % 5][col2]
    else:
        return key_table[row1][col2] + key_table[row2][col1]


def format_input_to_two_letters(plaintext):
    format_plaintext = ""
    plaintext = plaintext.replace(" ", "").upper()
    plaintext = list(plaintext)
    for i in range(1, len(plaintext)):
        if plaintext[i] == plaintext[i - 1] and (i - 1) % 2 == 0:
            plaintext.insert(i, 'X')
    plaintext = "".join(plaintext)
    i = 0
    while i < len(plaintext) - 2:
        format_plaintext += plaintext[i:i + 2] + " "
        i += 2
    if len(plaintext) % 2 == 0:
        format_plaintext += plaintext[i: len(plaintext)]
    else:
        format_plaintext += plaintext[len(plaintext) - 1] + 'Z'
    return format_plaintext


def undo_format(plaintext):
    if "X" in plaintext:
        plaintext = plaintext.replace("X", "")
    if "Z" in plaintext:
        plaintext = plaintext.replace("Z", "")
    return plaintext


def encrypt(secret_key, plaintext):
    key_table = construct_lookup_table(secret_key)
    plaintext = format_input_to_two_letters(plaintext)
    plaintext = plaintext.replace(" ", "")
    cipher = []
    i = 0
    while i <= len(plaintext) - 2:
        alpha1 = plaintext[i]
        alpha2 = plaintext[i + 1]
        ciphertext = calculate_position_to_encrypt(alpha1, alpha2, key_table)
        cipher.append(ciphertext)
        cipher.append(" ")
        i += 2
    return "".join(cipher)


def decrypt(secret_key, ciphertext):
    key_table = construct_lookup_table(secret_key)
    ciphertext = ciphertext.replace(" ", "")
    plaintext = []
    i = 0
    while i <= len(ciphertext) - 2:
        alpha1 = ciphertext[i]
        alpha2 = ciphertext[i + 1]
        plain = calculate_position_to_decrypt(alpha1, alpha2, key_table)
        plaintext.append(plain)
        plaintext.append(" ")
        i += 2
    result = "".join(plaintext)
    return undo_format(result)


key = input("Please Type the key: ")
ciphertext = encrypt(key, input("Please type the plaintext: "))
print("Cipher text is: ", ciphertext)
print("************* Decrypting Cipher Text *********************")
print("Plaintext is: ", decrypt(input("Please type the secret key: "), input("Please enter your cipher text: ")))
