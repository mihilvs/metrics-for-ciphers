import random
import os

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
            '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']

M = len(ALPHABET)

superscript_map = {
        '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', 
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'
    }

letter_to_index = {letter: index for index, letter in enumerate(ALPHABET)}

def get_index(letter):
    return letter_to_index[letter]

def find_values(file):
    
    def encrypt(file, a, b):
        file = open(file, 'r')
        words = [""]
        for line in file.readlines():
            for letter in line:
                if letter in superscript_map:
                    letter = superscript_map[letter]
                if letter in ALPHABET:

                    words[-1] += str((a * get_index(letter) + b) % M)
                    if words[-1].count("-") == 4:
                        words.append("")
                    else:
                        words[-1] += "-"
        if not words[-1]:
            words.pop()
        elif words[-1][-1] == "-":
            words[-1] = words[-1][:len(words[-1]) - 1]
        
        return " ".join(words)

    def decrypt(file):
        #https://blogs.sas.com/content/iml/2014/09/19/frequency-of-letters.html

        def freq_vector(file, a, b):
            file = open(file, "r")
            count = [0] * M
            total = 0

            for line in file.readlines():
                for string in line.split(" "):
                    for number in string.split("-"):
                        if number.isnumeric(): 
                            count[(a * int(number) + b) % M] += 1
                        total += 1
            for i in range(len(count)):
                count[i] /= total

            return count
       
        initial = freq_vector(file, 1, 0)
        return initial 

    enc_f = "./training_unciphered/" + file
    dec_f = "./training_ciphered/" + file
    a = 1  
    b = 0 
    
    with open(dec_f, 'w') as f:
        f.write(encrypt(enc_f, a, b))
    
    return decrypt(dec_f)

def main():

    for file in os.listdir("./training_unciphered"):
        print(find_values(file))
        
if __name__ == "__main__":
    main()

