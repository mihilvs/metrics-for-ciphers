import random
import os
import matplotlib.pyplot as plt

math = True
affine = False 

if affine: print("Affine over", end = " ")
else: print("Shift over", end = " ")

if math: print("|A| = 40")
else: print("|A| = 26")

print()

if math:
    training = "./training_"
else:
    training = ""

if math:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
                '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
else:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']

M = len(ALPHABET)

letter_to_index = {letter: index for index,
                   letter in enumerate(ALPHABET)}
def get_index(letter):
    return letter_to_index[letter]

if not math:
    alphabet_freq = [.0804, .0148, .0334, .0382, .1249, .0240, .0187,
                            .0505, .0757, .0016, .0054, .0407, .0251, .0723,
                            .0764, .0214, .0012, .0628, .0651, .0928, .0273,
                            .0105, .0168, .0023, .0166, .0009]
else:
    alphabet_freq = [0.07144860515156036, 0.015766482807539284,
                     0.033337754349652936, 0.02847339104138418,
                     0.11194627104174712, 0.028861942334825003,
                     0.013974503456265162, 0.04064444007383542, 
                     0.07478438205266631, 0.0018111934262244904, 
                     0.003932480673175791, 0.03551641695930326, 
                     0.02462310391105164, 0.06914051439814713, 
                     0.07176510366393729, 0.023252766760077315, 
                     0.003129225595389476, 0.054355016861685077,
                     0.06363995171929944, 0.08912288548438016, 
                     0.026358775348235094, 0.010798843846412292,
                     0.01482259137560234, 0.010701706023052086,
                     0.015494016550256949, 0.0016516098592755813,
                     0.007911662222967065, 0.0126999698178906,
                     0.009149368884353418, 0.005170187334562144, 
                     0.004088061307843372, 0.0037133868463111513,
                     0.0038548237869180436, 0.0026662197615159693,
                     0.0025325218233196423, 0.002711853189523099,
                     0.0025685482138515865, 0.0025685482138515865,
                     0.00015504691036340488, 0.0008558269217477443]
def find_values(file, norm):
    def length(vector):
        return (sum(i**2 for i in vector)) ** .5

    def determine_bijection(a,b,c,d):
        found = {i : -1 for i in range(M)}
        for x in range(0, M):
            found[x] = ((a * (x**3) + b * (x ** 2) + c * x + d) % M)
        duplicates = set()
        for i in range(M):
            if found[i] in duplicates:
                return False, found
            duplicates.add(found[i])
        return True, found

    def encrypt(file, a, b, c, d):
        file = open(file, 'r')
        words = [""]
        for line in file.readlines():
            for letter in line:
                if letter.isalpha():
                    letter = letter.lower()
                if letter in ALPHABET:
                    x = get_index(letter)
                    words[-1] += str((a * (x**3) + b * (x ** 2)
                                      + c * x + d) % M)
                                      
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

        def freq_vector(file, a, b, c, d):
            file = open(file, "r")
            count = [0] * M
            total = 0

            for line in file.readlines():
                for string in line.split(" "):
                    for number in string.split("-"):
                        if number.isnumeric(): 
                            count[int(number)] += 1
                        total += 1
            for i in range(len(count)):
                count[i] /= total
            return count

        def compare_abs(vector, mapping):
            res = 0
            for i in range(M):
                res += abs(vector[mapping[i]] - alphabet_freq[i])**norm
            return (res ** (1/norm))


        original_map = {i : i for i in range(M)}

        soln_vec = freq_vector(file, 0, 0, 1, 0) 
        abs_beta, abs_alpha = (float("inf"), 
                               compare_abs(soln_vec, original_map))
        if affine: c_range = range(M)
        else: c_range = range(1,2)

        for a in range(0,1):
            for b in range(0,1):
                for c in c_range:
                    for d in range(M):
                        bijection, mapping = determine_bijection(a,b,c,d)
                        if (bijection and mapping != original_map):
                            
                            abs_beta = min(abs_beta, 
                                           compare_abs(soln_vec, mapping))

        return (abs_alpha, abs_beta)

    enc_f = "./" + training + "unciphered/" + file
    dec_f = "./" + training + "ciphered/" + file
    a = 0  #random.randrange(1, 26)
    b = 0
    c = 1
    d = 0

#    with open(dec_f, 'w') as f:
#        f.write(encrypt(enc_f, a, b, c, d))

    return decrypt(dec_f) 
       

def main():
    norm = 1
    xpoints = []
    ypoints = []
    while norm <= 10:
        absolute_alpha, absolute_beta = 0, float('inf')
        for file in os.listdir("./" + training + "unciphered"):

            (abs_alpha, abs_beta) = find_values(file, norm)

            absolute_alpha, absolute_beta = (max(absolute_alpha, abs_alpha),
                                         min(absolute_beta, abs_beta))
        absolute_difference = (2 * (-absolute_alpha + absolute_beta) 
                               / (absolute_alpha + absolute_beta))
        print(f"For L({norm}): \n"
          f"Alpha = {absolute_alpha} \n"
          f"Beta = {absolute_beta}")
        print(f"For L({norm}): \n"
              f"Normalized Difference = {absolute_difference} \n")
        xpoints.append(norm)
        ypoints.append(absolute_difference)
        norm += 1
    return xpoints, ypoints
if __name__ == "__main__":
    xshift, yshift = main()
    plt.plot(xshift, yshift, label="Shift")

    affine = True
    
    xaffine, yaffine = main()
    plt.plot(xaffine, yaffine, label = "Affine")
    
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel("Value of K in LK Norm")
    plt.ylabel("Normalized Difference")
    plt.title("LK Norms against Cipher Cracking Math Textbooks")
    plt.legend(loc="upper right")
    plt.show()

