import random
import os
import sys


def determine_bijection(a,b,c,d,e,f, M):
    found = set()
    for x in range(0, M):
        found.add((a * (x**5) + b * (x**4) + c * (x ** 3) + (d * (x ** 2)) + e * x + f) % M)
    return len(found) == M
    
def find_similar(a,b,c,d,e,f, M):
    found = []
    for k in range(0,1):
        for i in range(M):
            for j in range(M):
                if determine_bijection(0, 0,0, 0, i,j, M):
                    temp_found = True
                    for x in range(M):
                        if ((a * (x**5) + b * (x**4) + c * (x ** 3) + 
                             (d * (x ** 2)) + e * x + f) % M) != ((k * (x ** 2)
                                                                   + i * x + j)
                                                                  % M):
                            temp_found = False 
                    if temp_found and (b,c,d) != (k,i,j): found.append(
                            (0, k, i, j)) 
#    if found: 
#        print(f"{(a, b, c, d, e, f)} is the same function as {found}")
#    else:
#        print(f"{(a, b, c, d, e, f)} is not affine")
def main():
    M = 26
    count = 0
    for a in range(1, M):
        for b in range(1, M):
            for c in range(M):
                for d in range(M):
                    for e in range(M):
                        for f in range(0,1):
                            if determine_bijection(a, b,c,d,e,f, M):
                                count += 1
                                find_similar(a, b, c,d,e,f, M)
    print(f"There were {count} bijections")
    print("DONE")


if __name__ == "__main__":
    main()
