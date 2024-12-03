import random
import os
import sys


def determine_bijection(a,b,c, M):
    found = set()
    for x in range(0, M):
        found.add((a * (x**2) + b * x + c * (x**3)) % M)
    return len(found) == M
    
def find_similar(a,b,c, M):
    found = [] 
    for i in range(0, M):
        for j in range(0, M):
            if determine_bijection(0, i, 0, M):
                temp_found = True
                for x in range(0, M):
                    if (a * (x**2) + b * x) % M != (i * x + j) % M:
                        temp_found = False 
                if temp_found: found.append((0, i, j)) 
    if found: 
        print(f"{(a, b, c)} is the same function as {found}")
    else:
        print(f"{(a, b, c)} is not affine")
def main():
    M = 40
    for c in range(0, 1):
        for a in range(1, M):
            for b in range(0, M):
                if determine_bijection(a, b, c, M):
                    find_similar(a, b, c, M)
    print("DONE")


if __name__ == "__main__":
    main()
