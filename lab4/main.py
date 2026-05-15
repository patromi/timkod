import math
import os
from collections import Counter

def joint_entropy(data, n):
    if n == 0:
        return 0.0
    
    ngrams = [tuple(data[i:i+n]) for i in range(len(data) - n + 1)]
    counts = Counter(ngrams)
    total = len(ngrams)
    
    if total == 0:
        return 0.0
        
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def conditional_entropy(data, order):
    if order == 0:
        return joint_entropy(data, 1)

    h_n_plus_1 = joint_entropy(data, order + 1)
    h_n = joint_entropy(data, order)
    
    return h_n_plus_1 - h_n

def analyze_file(filepath, max_items=50000):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read() 
            
        print(f"Plik: {filepath}")

        chars = list(text[:max_items * 5])
        print("Entropia znaków:")
        for order in range(6):
            ent = conditional_entropy(chars, order)
            print(f"  Rząd {order}: {ent:.4f} bitów/znak")
            
        words = text.split()[:max_items]
        print("Entropia słów:")
        for order in range(4):
            ent = conditional_entropy(words, order)
            print(f"  Rząd {order}: {ent:.4f} bitów/słowo")
        print("")
        
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filepath}\n")


def main():
    data_dir = os.listdir("data")
    for filename in data_dir:
        analyze_file(os.path.join("data", filename))
    
    sample_dir = os.listdir("samples")
    for filename in sample_dir:
        analyze_file(os.path.join("samples", filename))

if __name__ == "__main__":
    main()