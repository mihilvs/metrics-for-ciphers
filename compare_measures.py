import random
import os
import numpy as np
from math import log
import constants

cipher_math = False
affine = True 

if affine: print("Affine over", end = " ")
else: print("Shift over", end = " ")

if cipher_math: print("|A| = 40")
else: print("|A| = 26")

print()

if cipher_math:
    training = "./training_"
    ALPHABET = constants.math_ALPHABET
    alphabet_freq = constants.math_freq
else:
    training = ""
    ALPHABET = constants.lower_ALPHABET
    alphabet_freq = constants.lowercase_freq

M = len(ALPHABET)

letter_to_index = {letter: index for index,
                   letter in enumerate(ALPHABET)}
def length(vector):
    return (sum(i**2 for i in vector)) ** .5

distance_measures = {"L1": { "func": lambda v, m:
                           sum(abs(v[m[i]] - alphabet_freq[i])
                               for i in range(M))},
                    "L2": { "func": lambda v, m:
                           np.sqrt(sum(abs(v[m[i]] - alphabet_freq[i])**2
                               for i in range(M)))},
                    "L3": { "func": lambda v, m:
                           (sum(abs(v[m[i]] - alphabet_freq[i])**3
                               for i in range(M)))**(1/3)},
                    "L4": { "func": lambda v, m:
                           (sum(abs(v[m[i]] - alphabet_freq[i])**4
                               for i in range(M)))**(1/4)},
                    "Kullback-Leibler": { "func": lambda v, m:
                           sum(v[m[i]] * log(v[m[i]] / alphabet_freq[i])
                               for i in range(M) if v[m[i]] != 0)},
                    "Chi-Squared": { "func": lambda v, m:
                           .5 * sum((abs(v[m[i]] - alphabet_freq[i])**2
                                / (v[m[i]] + alphabet_freq[i]))
                               for i in range(M))},
                    "Bhattacharyya": { "func": lambda v, m:
                           -1 * log(sum(np.sqrt(v[m[i]] * alphabet_freq[i])
                                        for i in range(M)))
                               },
                    "Taneja": { "func": lambda v, m: 
                               sum(((v[m[i]] + alphabet_freq[i]) / 2)
                                   * np.log((v[m[i]] + alphabet_freq[i]) / 
                                            (2 * np.sqrt(v[m[i]] * 
                                                         alphabet_freq[i])))
                                   for i in range(M) 
                                   if v[m[i]] > 0 and alphabet_freq[i] > 0)
                               },
                    "Optimized": { "func": lambda v, m: 
                           sum(constants.optimal[i] * v[m[i]] *
                               log(v[m[i]] / alphabet_freq[i])
                               for i in range(M) if v[m[i]] != 0)}
                     }

similarity_measures = {"Dot Product": { "func": lambda v, m:
                           sum(v[m[i]] * alphabet_freq[i] for i in range(M))
                               },
                        "Cosine Similarity": { "func": lambda v, m:
                           (sum(v[m[i]] * alphabet_freq[i] for i in range(M))
                                / (length(v) * length(alphabet_freq)))
                               },

                        "Intersection": { "func": lambda v, m:
                           (sum(min(v[m[i]], alphabet_freq[i])
                                for i in range(M)))
                               },
                       }
def get_index(letter):
    return letter_to_index[letter]


def find_values(file):

    
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
        def compare_measure(name, vector, mapping):
            if name in distance_measures:
                func = distance_measures[name]["func"]
                return func(vector, mapping)
            else:
                func = similarity_measures[name]["func"]
                return func(vector, mapping)
        original_map = {i : i for i in range(M)}

        soln_vec = freq_vector(file, 0, 0, 1, 0) 
        distance_values = {name: {"beta": float("inf"), "alpha": 
                                  compare_measure(name, 
                                                  soln_vec,original_map)}
                           for name in distance_measures}
        similarity_values = {name: {"beta": 0, "alpha": 
                          compare_measure(name, soln_vec, original_map)}
                   for name in similarity_measures}

        if affine: c_range = range(M)
        else: c_range = range(1,2)

        for c in c_range:
            for d in range(M):
                bijection, mapping = determine_bijection(a,b,c,d)
                if (bijection and mapping != original_map):
                    for name in distance_measures:
                        distance_values[name]["beta"] = min(
                                distance_values[name]["beta"],
                                compare_measure(name, soln_vec, mapping)
                                )

                    for name in similarity_measures:
                        similarity_values[name]["beta"] = max(
                                similarity_values[name]["beta"],
                                compare_measure(name, soln_vec, mapping)
                                )
                    
        return (distance_values, similarity_values)

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
    ovr_distance_values = {name: {"alpha": 0, "beta": float("inf")}
                       for name in distance_measures}
    ovr_similarity_values = {name: {"alpha": float("inf"), "beta": 0}
               for name in similarity_measures}

    for file in os.listdir("./" + training + "unciphered"):

        (distance_values, similarity_values) = find_values(file)
        for name in distance_measures:
            measure = ovr_distance_values[name]
            comp_meas = distance_values[name]
            measure["alpha"],measure["beta"] = (max(measure["alpha"],
                                                   comp_meas["alpha"]),
                                                min(measure["beta"],
                                                    comp_meas["beta"])) 
        for name in similarity_measures:
            measure = ovr_similarity_values[name]
            comp_meas = similarity_values[name]
            measure["alpha"],measure["beta"] = (min(measure["alpha"],
                                                   comp_meas["alpha"]),
                                                max(measure["beta"],
                                                    comp_meas["beta"]))

    for name in distance_measures:
        alpha = ovr_distance_values[name]['alpha']
        beta = ovr_distance_values[name]['beta']

        print(f"For {name}: \n"
              f"Alpha = {ovr_distance_values[name]['alpha']} \n"
              f"Beta = {ovr_distance_values[name]['beta']} \n"
              f"Normed = {2 * (-alpha + beta) / (alpha + beta)}")
    for name in similarity_measures:
        alpha = ovr_similarity_values[name]['alpha']
        beta = ovr_similarity_values[name]['beta']

        print(f"For {name}: \n"
              f"Alpha = {ovr_similarity_values[name]['alpha']} \n"
              f"Beta = {ovr_similarity_values[name]['beta']} \n"
              f"Normed = {2 * (alpha - beta) / (alpha + beta)}")
 
if __name__ == "__main__":
    main()

