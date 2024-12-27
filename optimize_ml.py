import random
import os
import numpy as np
from math import log
import tensorflow as tf
import constants

cipher_math = False 
affine = False 

if affine: 
    print("Affine over", end = " ")
    c_range = range(M)
else: 
    c_range = range(1,2)
    print("Shift over", end = " ")

if cipher_math:
    print("|A| = 40 \n")
    training = "./training_"
    ALPHABET = constants.math_ALPHABET
    alphabet_freq = constants.math_freq
else:
    print("|A| = 26 \n")
    training = ""
    ALPHABET = constants.lower_ALPHABET
    alphabet_freq = constants.lowercase_freq

M = len(ALPHABET)
original_map = {i:i for i in range(M)}
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
                    "Kullback-Leibler": { "func": lambda v, m, a:
                           sum(a[i] * v[m[i]] * log(v[m[i]] 
                                                    / alphabet_freq[i])
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
                               }
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

def loss_fn_multi_instance(vectors, a):
    total_loss = 0
    ovr_alpha, ovr_beta = 0, float('inf')
    for v in vectors:  
        alpha = weighted_divergence(v, original_map, a)  
        for c in c_range:
            for d in range(M):
                bijection, mapping = determine_bijection(0,0,c,d)
                if (bijection and mapping != original_map):

                     beta = tf.reduce_min([weighted_divergence(v, 
                                                               mapping, a)
                              for i in range(1, 26)]) 
        ovr_alpha, ovr_beta = max(ovr_alpha, alpha), min(ovr_beta, beta)
    return -2 * (-ovr_alpha + ovr_beta) / (ovr_alpha + ovr_beta)

def weighted_divergence(v, m, a):
    return distance_measures["Kullback-Leibler"]["func"](v, m, a)

def freq_vector():
    num_characters = 1000 
    sample = np.random.choice(ALPHABET, 
                              size=num_characters, p=alphabet_freq)
    sample_frequencies = [np.sum(sample == letter)
                          for letter in ALPHABET]
    sample_percentages = [(count / num_characters)
                          for count in 
                          sample_frequencies]
    return sample_percentages


def main():
    batch_size = 32
    a = tf.Variable(tf.ones([M]), dtype=tf.float32, trainable=True)
    optimizer = tf.optimizers.Adam(learning_rate=0.01)
    
    freq_vectors_list = []
    for i in range(192):
        freq_vectors_list.append(freq_vector())

    print("Beginning Machine Learning")
    num_batches = len(freq_vectors_list) // batch_size
    for step in range(100):
        total_loss = 0
        for batch_index in range(num_batches):
            start = batch_index * batch_size
            end = start + batch_size
            batch_vectors = freq_vectors_list[start:end]
            with tf.GradientTape() as tape:
                batch_loss = loss_fn_multi_instance(batch_vectors, a)
                total_loss += batch_loss
            gradients = tape.gradient(batch_loss, [a])
            optimizer.apply_gradients(zip(gradients, [a]))
        print(f"Step: {step}, Loss: {total_loss.numpy() / num_batches}," 
              f"a: {np.array2string(a.numpy(), separator=', ')}")
    
    print()
    print(f"Optimized: {a.numpy()}")
 
if __name__ == "__main__":
    main()

