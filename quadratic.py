import random
import os


def find_values(file):

    def determine_bijection(a,b,c):
        found = set()
        for x in range(0, 26):
            found.add((a * (x**2) + b * x + c) % 26)
        return len(found) == 26

    def encrypt(file, a, b, c):
        file = open(file, 'r')
        words = [""]
        for line in file.readlines():
            for letter in line:
                if letter.isalpha():
                    letter = letter.lower()
                    words[-1] += str((a * (ord(letter) - 97)**2 + 
                                      b * (ord(letter) - 97) + c) % 26)
                                      
                    if words[-1].count("-") == 4:
                        words.append("")
                    else:
                        words[-1] +=  "-"
        if not words[-1]:
            words.pop()
        elif words[-1][-1] == "-":
            words[-1] = words[-1][:len(words[-1]) - 1]
        
        return " ".join(words)

    def decrypt(file):
        #https://blogs.sas.com/content/iml/2014/09/19/frequency-of-letters.html
        english_freq = [.0804, .0148, .0334, .0382, .1249, .0240, .0187,
                        .0505, .0757, .0016, .0054, .0407, .0251, .0723,
                        .0764, .0214, .0012, .0628, .0651, .0928, .0273,
                        .0105, .0168, .0023, .0166, .0009]

        def freq_vector(file, a, b, c):
            file = open(file, "r")
            count = [0] * 26
            total = 0

            for line in file.readlines():
                for string in line.split(" "):
                    for number in string.split("-"):
                        if number.isnumeric(): 
                            count[(a * int(number)**2 + 
                                   b * int(number) + c) % 26] += 1
                        total += 1
            for i in range(len(count)):
                count[i] /= total
            return count

        def compare_abs(vector):
            res = 0
            for i in range(26):
                res += abs(vector[i] - english_freq[i])
            return res

        def compare_square(vector):
            res = 0
            for i in range(26):
                res += (vector[i] - english_freq[i])**2
            return res

        def compare_dot(vector):
            res = 0
            for i in range(26):
                res += (vector[i] * english_freq[i])
            return res

        soln_vec = freq_vector(file, 0, 1, 0) 
        abs_beta, abs_alpha = float("inf"), compare_abs(soln_vec)
        sqr_beta, sqr_alpha = float("inf"), compare_square(soln_vec)
        dot_beta, dot_alpha = 0, compare_dot(soln_vec)

        for a in [0, 13]:
            for b in range(0, 26):
                for c in range(0, 26):
                    if (determine_bijection(a,b,c) and 
                        (vec := freq_vector(file, a, b, c)) != soln_vec):
                        abs_beta = min(abs_beta, compare_abs(vec))
                        sqr_beta = min(sqr_beta, compare_square(vec))
                        dot_beta = max(dot_beta, compare_dot(vec))

        return (abs_alpha, abs_beta, sqr_alpha,
                sqr_beta, dot_alpha, dot_beta)

    enc_f = "./unciphered/" + file
    dec_f = "./ciphered/" + file
    a = 0  #random.randrange(1, 26)
    b = 1
    c = 0
    
    #with open(dec_f, 'w') as f:
    #    f.write(encrypt(enc_f, s))

    return decrypt(dec_f) 
       

def main():
    absolute_alpha, absolute_beta = 0, float('inf')
    square_alpha, square_beta = 0, float('inf')
    dprod_alpha, dprod_beta = float("inf"), 0

    for file in os.listdir("./unciphered"):

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
