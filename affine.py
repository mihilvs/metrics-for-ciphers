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

alphabet_freq = [0.0716141459118763, 0.013541810396956157,
                 0.029664948512737686, 0.027217341173455326,
                 0.11749400142831719, 0.025147297258764995,
                 0.01527362041044946, 0.04415066747117392,
                 0.07693444718913535, 0.0016121827131668361,
                 0.004470128079870396, 0.036336874410671675,
                 0.025857850648101383, 0.0702179478313537,
                 0.07326074195801377, 0.021333316727534565,
                 0.0024433466409145687, 0.05713858708031711,
                 0.060077485716008724, 0.08928195105899658,
                 0.027408744853977672, 0.011569434798696751,
                 0.015138589046793284, 0.008182835088358691,
                 0.014596824862027116, 0.0030234571109908647,
                 0.007859677504463081, 0.014130114517739746,
                 0.008933045747118375, 0.005086946105115362,
                 0.0037402376748647964, 0.003052954253537117,
                 0.0023541997212192284, 0.0019664761697501558,
                 0.0016980521725792597, 0.0014538813815019487,
                 0.003734338246355546, 0.002018915534276827,
                 0.00026186907660506243, 0.0007207135162134321]


def find_values(file):
    
    def determine_bijection(a,b,c):
        found = set()
        for x in range(0, M):
            found.add((a * (x**2) + b * x + c) % M)
        return len(found) == M


    def encrypt(file, a, b):
        file = open(file, 'r')
        words = [""]
        for line in file.readlines():
            for letter in line:
                if letter in superscript_map:
                    letter = superscript_map[letter]
                if letter.isalpha():
                    letter = letter.lower()
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

        def compare_abs(vector):
            res = 0
            for i in range(M):
                res += abs(vector[i] - alphabet_freq[i])
            return res

        def compare_square(vector):
            res = 0
            for i in range(M):
                res += (vector[i] - alphabet_freq[i])**2
            return res

        def compare_dot(vector):
            res = 0
            for i in range(M):
                res += (vector[i] * alphabet_freq[i])
            return res
       
        soln_vec = freq_vector(file, 1, 0)
        abs_beta, abs_alpha = float("inf"), compare_abs(soln_vec)
        sqr_beta, sqr_alpha = float("inf"), compare_square(soln_vec)
        dot_beta, dot_alpha = 0, compare_dot(soln_vec)

        for a in range(1, M):
            for b in range(0, M):
                if (determine_bijection(0, a, b) and
                    ((vec := freq_vector(file, a, b)) != soln_vec)):
                    abs_beta = min(abs_beta, compare_abs(vec))
                    sqr_beta = min(sqr_beta, compare_square(vec))
                    dot_beta = max(dot_beta, compare_dot(vec))

        return (abs_alpha, abs_beta, sqr_alpha,
                sqr_beta, dot_alpha, dot_beta)
    
    enc_f = "./training_unciphered/" + file
    dec_f = "./training_ciphered/" + file
    a = 1  
    b = 0 
    
    #with open(dec_f, 'w') as f:
     #   f.write(encrypt(enc_f, a, b))
    
    return decrypt(dec_f)

def main():
    absolute_alpha, absolute_beta = 0, float('inf')
    square_alpha, square_beta = 0, float('inf')
    dprod_alpha, dprod_beta = float("inf"), 0

    for file in os.listdir("./training_ciphered"):

        (abs_alpha, abs_beta, sqr_alpha,
     sqr_beta, dot_alpha, dot_beta) = find_values(file)

        #print("Abs:", abs_alpha, abs_beta)
        absolute_alpha, absolute_beta = (max(absolute_alpha, abs_alpha),
                                     min(absolute_beta, abs_beta))
        #print("Sqr:", sqr_alpha, sqr_beta)
        square_alpha, square_beta = (max(square_alpha, sqr_alpha),
                                 min(square_beta, sqr_beta))
        #print("Dot Prod:", dot_alpha, dot_beta) 
        dprod_alpha, dprod_beta = (min(dprod_alpha, dot_alpha),
                               max(dprod_beta, dot_beta))

    print(f"For Absolute Value: \n"
          f"Alpha = {absolute_alpha} \n"
          f"Beta = {absolute_beta}")
    print(f"For Squared Value: \n"
          f"Alpha = {square_alpha} \n"
          f"Beta = {square_beta}")
    print(f"For Dot Product: \n"
          f"Alpha = {dprod_alpha} \n"
          f"Beta = {dprod_beta}")

if __name__ == "__main__":
    main()

