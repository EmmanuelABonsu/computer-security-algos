from collections import Counter
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import PyQt5
import string

"""
This function generates the the single letter frequency and plots the resulting distribution
"""

"""
This function computes the letter frequencies in the cipher text and plots the comparison between with the English
alphabet. Result of the plot is displayed in plot.py
"""


def find_relative_frequency_with_respect_to_english(cipher_text):
    cipher_text = cipher_text.upper()
    counter = Counter(cipher_text)
    total_count = sum(counter.values())
    relative_frequency = {}
    for key in counter:
        relative_frequency[key] = (counter[key] / total_count) * 100
    sorted_relative_frequency = sorted(relative_frequency.items(), key=lambda x: -x[1])
    english_letter_frequency = {'E': 12.0,
                                'T': 9.10,
                                'A': 8.12,
                                'O': 7.68,
                                'I': 7.31,
                                'N': 6.95,
                                'S': 6.28,
                                'R': 6.02,
                                'H': 5.92,
                                'D': 4.32,
                                'L': 3.98,
                                'U': 2.88,
                                'C': 2.71,
                                'M': 2.61,
                                'F': 2.30,
                                'Y': 2.11,
                                'W': 2.09,
                                'G': 2.03,
                                'P': 1.82,
                                'B': 1.49,
                                'V': 1.11,
                                'K': 0.69,
                                'X': 0.17,
                                'Q': 0.11,
                                'J': 0.10,
                                'Z': 0.07}
    new_dict = {(key1, key2) for (key1, value1), (key2, value2) in
                zip(sorted_relative_frequency, english_letter_frequency.items())}
    new_dict = dict(new_dict)
    # Plotting letter relative frequencies
    fig, ax = plt.subplots(2, 1)
    fig.suptitle("Relative Letter Frequencies", fontsize=16)
    ax[0].bar(*zip(*counter.most_common()), width=.5, color='g')
    ax[1].bar(english_letter_frequency.keys(), english_letter_frequency.values(), .5, color='r')
    plt.savefig('plot.png')
    return sorted_relative_frequency, new_dict


"""
This function attempts to decrypt cipher text with letter frequency analysis. Switches to ceaser cipher if the user 
doesn't find any meaningful decryption
"""


def decrypt_cipher(cipher, iterations):
    sorted_relative_frequency, unigram = find_relative_frequency_with_respect_to_english(cipher)
    original_ciphertext = list(cipher.upper())
    cipher_text_ceaser = cipher.upper()
    cipher = cipher.upper()
    cipher = list(cipher)
    # Substitution with single letter frequency table
    j = 0
    while j < iterations:
        old_character = sorted_relative_frequency[j][0]
        print("Replacing", old_character, "with =====> ", unigram.get(old_character))
        cipher = list(cipher)
        for index, character in enumerate(cipher):
            if character == old_character and original_ciphertext[index] == cipher[index]:
                cipher[index] = unigram.get(character)
        print("************************************", "Iteration", str(j), "******************************************")
        print("".join(cipher))
        j += 1
    user_response = input("Is the resulting plaintext isn't meaningful(y/n): ")
    if user_response == 'n':
        ceaser = input("Would you like to decrypt with a Ceaser Cipher(y/n): ")
        if ceaser == 'y':
            print(
                "*****************************************************************************************************")
            print(
                "*****************************************************************************************************")
            print("***************************** Decrypting with Ceaser Cipher ***************************************")
            # Find the shift shift in the alphabets that maps J to E or Y to T (as shown in the frequency graph)
            shift = 0
            while shift <= 26:
                if chr((ord('J') + shift - 65) % 26 + 65) == 'E':
                    break
                shift += 1
            alphabets = string.ascii_uppercase
            for letter in alphabets:
                cipher_text_ceaser = cipher_text_ceaser.replace(letter, chr((ord(letter) + shift - 65) % 26 + 65))
                print(
                    "*************************************************************************************************")
                print("Replacing ", letter, "with", chr((ord(letter) + shift - 65) % 26 + 65))
                print(cipher_text_ceaser)
            return cipher_text_ceaser

    else:
        return


user_val = input("Please type the cipher text: ")
iterations =input("Please type the number of iterations you want: ")
print(decrypt_cipher(user_val, int(iterations)))
print("***************************************************************************************************************")
