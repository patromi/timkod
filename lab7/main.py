import os

def compress_lzw(data, max_dict_size= None):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(256)}
    
    w = b""
    result = []
    
    for byte in data:
        c = bytes([byte])
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            if max_dict_size is None or dict_size < max_dict_size:
                dictionary[wc] = dict_size
                dict_size += 1
            w = c
            
    if w:
        result.append(dictionary[w])
    return result

def decompress_lzw(compressed, max_dict_size = None):
    if not compressed:
        return b""
        
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(256)}
    
    w = bytes([compressed[0]])
    result = bytearray(w)
    
    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + bytes([w[0]])
        else:
            raise ValueError(f"Błędny kod kompresji: {k}")
            
        result.extend(entry)
        
        if max_dict_size is None or dict_size < max_dict_size:
            dictionary[dict_size] = w + bytes([entry[0]])
            dict_size += 1
            
        w = entry
        
    return bytes(result)

def get_byte_length(max_dict_size: int) -> int:
    if max_dict_size == 2**12:
        return 2
    elif max_dict_size == 2**18:
        return 3
    else:
        return 4

def save_compressed(compressed_codes, filename, max_dict_size):
    byte_length = get_byte_length(max_dict_size)
    with open(filename, 'wb') as f:
        for code in compressed_codes:
            f.write(code.to_bytes(byte_length, byteorder='big'))

def load_compressed(filename, max_dict_size):
    byte_length = get_byte_length(max_dict_size)
    compressed_codes = []
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(byte_length)
            if not bytes_read:
                break
            compressed_codes.append(int.from_bytes(bytes_read, byteorder='big'))
    return compressed_codes

def main():
    files_to_test = os.listdir("data/")
    dict_limits = {
        "2^12": 2**12,
        "2^18": 2**18,
        "Brak limitu": None
    }
    
    for filename in files_to_test:
        print(f"\nTestowanie pliku: {filename}")
        if not os.path.exists(f"data/{filename}"):
            print(f"Plik {filename} nie istnieje w obecnym katalogu.")
            continue
            
        with open(f"data/{filename}", 'rb') as f:
            original_data = f.read()
        
        original_size = len(original_data)
        print(f"Oryginalny rozmiar: {original_size} bajtów")
        
        for limit_name, limit_val in dict_limits.items():
            
            compressed_codes = compress_lzw(original_data, limit_val)
            
            comp_filename = f"{filename}_{limit_name.split()[0]}.lzw"
            save_compressed(compressed_codes, comp_filename, limit_val)
            comp_size = os.path.getsize(comp_filename)
            
            loaded_codes = load_compressed(comp_filename, limit_val)
            decompressed_data = decompress_lzw(loaded_codes, limit_val)
            
            is_correct = original_data == decompressed_data
            ratio = (comp_size / original_size) * 100
            
            print(f"\nLimit słownika: {limit_name}")
            print(f"Rozmiar po kompresji: {comp_size} bajtów ({ratio:.2f}% oryginału)")
            print(f"Dekompresja poprawna: {'TAK' if is_correct else 'NIE'}")

if __name__ == "__main__":
    main()