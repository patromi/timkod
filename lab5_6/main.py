import math
import ast
import heapq
import os
from bitarray import bitarray

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def create_huffman_code(frequencies):
    if not frequencies:
        return {}

    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        return {heap[0].char: '0'}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)

    codes = {}
    def generate_codes(node, current_code):
        if node is None: 
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
            
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(heap[0], "")
    return codes

def create(frequencies):
    unique_chars = list(frequencies.keys())
    n = len(unique_chars)
    code_len = math.ceil(math.log2(n)) if n > 1 else 1
    
    codes = {}
    for i, char in enumerate(unique_chars):
        bin_str = format(i, f'0{code_len}b')
        codes[char] = bin_str
        
    return codes


def encode(text, codes):
    encoded_bits = bitarray()
    for char in text:
        encoded_bits.extend(codes[char])
    return encoded_bits

def decode(encoded_bits, codes):
    inv_codes = {v: k for k, v in codes.items()}
    code_len = len(next(iter(codes.values())))
    decoded_text = []
    
    for i in range(0, len(encoded_bits), code_len):
        chunk = encoded_bits[i:i+code_len].to01()
        if chunk in inv_codes:
            decoded_text.append(inv_codes[chunk])
            
    return "".join(decoded_text)

def decode_huffman(encoded_bits, codes):
    inv_codes = {v: k for k, v in codes.items()}
    decoded_text = []
    current_bits = ""
    
    for bit in encoded_bits.to01():
        current_bits += bit
        if current_bits in inv_codes:
            decoded_text.append(inv_codes[current_bits])
            current_bits = ""
            
    return "".join(decoded_text)

def save(data_bin_filename, data_txt_filename, codes_filename, codes, encoded_bits):
    with open(codes_filename, 'w', encoding='utf-8') as f:
        f.write(f"{len(encoded_bits)}\n")
        f.write(f"{len(codes)}\n")
        for char, code in codes.items():
            f.write(f"{repr(char)}={code}\n")
            
    with open(data_bin_filename, 'wb') as f:
        encoded_bits.tofile(f)
        
    with open(data_txt_filename, 'w', encoding='utf-8') as f:
        f.write(encoded_bits.to01())

def load(data_bin_filename, codes_filename):
    codes = {}
    encoded_bits = bitarray()
    
    with open(codes_filename, 'r', encoding='utf-8') as f:
        bit_length = int(f.readline().strip())
        dict_size = int(f.readline().strip())
        
        for _ in range(dict_size):
            line = f.readline().rstrip('\n')
            char_repr, code = line.rsplit('=', 1)
            char = ast.literal_eval(char_repr)
            codes[char] = code
            
    with open(data_bin_filename, 'rb') as f:
        encoded_bits.fromfile(f)
        
    encoded_bits = encoded_bits[:bit_length]
        
    return codes, encoded_bits

if __name__ == "__main__":
    with open("dane/norm_wiki_sample.txt", 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    frequencies = {}
    for char in original_text:
        frequencies[char] = frequencies.get(char, 0) + 1
        
    print(f"Rozmiar oryginału: {len(original_text.encode('utf-8'))} bajtów\n")

    print("Kodowanie podstawowe:")
    basic_codes = create(frequencies)
    encoded_basic = encode(original_text, basic_codes)
    
    save("basic_comp.bin", "basic_comp_bits.txt", "basic_codes.txt", basic_codes, encoded_basic)
    
    loaded_codes_basic, loaded_encoded_basic = load("basic_comp.bin", "basic_codes.txt")
    decoded_text_basic = decode(loaded_encoded_basic, loaded_codes_basic)
    
    bin_size_basic = os.path.getsize("basic_comp.bin")
    txt_size_basic = os.path.getsize("basic_codes.txt")
    
    print(f"Czy odkodowano poprawnie?: {original_text == decoded_text_basic}")
    print(f"Rozmiar binarki: {bin_size_basic} bajtów")
    print(f"Całkowity rozmiar (bity + słownik): {bin_size_basic + txt_size_basic} bajtów")
    print(f"Stopień kompresji samych danych: {len(original_text.encode('utf-8')) / bin_size_basic:.2f}x\n")

    print("Kodowanie HUFFMANA:")
    codes_huffman = create_huffman_code(frequencies)
    encoded_huffman = encode(original_text, codes_huffman)
    
    save("huffman_comp.bin", "huffman_comp_bits.txt", "huffman_codes.txt", codes_huffman, encoded_huffman)
    
    loaded_codes_huffman, loaded_encoded_huffman = load("huffman_comp.bin", "huffman_codes.txt")
    decoded_text_huffman = decode_huffman(loaded_encoded_huffman, loaded_codes_huffman) 
    
    bin_size_huffman = os.path.getsize("huffman_comp.bin")
    txt_size_huffman = os.path.getsize("huffman_codes.txt")
    
    print(f"Czy odkodowano poprawnie?: {original_text == decoded_text_huffman}")
    print(f"Rozmiar zakodowanego pliku binarnego: {bin_size_huffman} bajtów")
    print(f"Całkowity rozmiar bity + kody: {bin_size_huffman + txt_size_huffman} bajtów")
    print(f"Stopień kompresji samych danych: {len(original_text.encode('utf-8')) / bin_size_huffman:.2f}x")

