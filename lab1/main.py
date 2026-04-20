import random

def generate_line(base_string, length, len_to_use = 27):
    base_string = base_string[:len_to_use]
    letters = {}
    for l in base_string:
        for letter in l:
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
    
    letters = dict(sorted(letters.items(), key=lambda item: item[1], reverse=True))
    probability_of_letters = {}
    for letter in letters:
        probability_of_letters[letter] = letters[letter] / len(base_string)
    return random.choices(list(probability_of_letters.keys()), list(probability_of_letters.values()), k=length)

def show_line_stats(line):  
    words = line.split()
    print("Number of words:", len(words))
    length_of_words = 0
    for word in words:
        length_of_words += len(word)
    print(f"Summary length of words: {length_of_words}")
    print(f"Average length of words: {length_of_words / len(words)}\n")


def build_markov_model(text, order):
    """
    Buduje model Markova n-tego rzędu z wykorzystaniem standardowych słowników.
    """
    model = {}
    for i in range(len(text) - order):
        state = text[i:i+order]
        next_char = text[i+order]
        
        if state not in model:
            model[state] = []
            
        model[state].append(next_char)
    return model

def generate_markov_text(model, order, length, seed=None):
    """
    Generuje tekst na podstawie wbudowanego słownika modelu.
    """
    if seed is None:
        current_state = random.choice(list(model.keys()))
        generated = current_state
    else:
        generated = seed
        
    while len(generated) < length:
        current_state = generated[-order:]
        
        if current_state in model:
            next_char = random.choice(model[current_state])
            generated += next_char
        else:
            current_state = random.choice(list(model.keys()))
            generated += current_state
            
    return generated[:length]


def main():
    # generator przyblizenia zerowego rzedu
    print("Zero-order approximation:")
    random_line = generate_line('abcdefghijklmnopqrstuvwxyz ', 50, 27)
    print("Generated line:", "".join(random_line))
    show_line_stats("".join(random_line))

    with open("data/norm_wiki_sample.txt", "r", encoding="utf-8") as f:
        line = f.read()[:50000]

    # generator przyblizenia pierwszego rzedu
    print("First order approximation on loaded text:")
    random_line_orig = generate_line(line, 50, 20000)
    print("Generated line:", "".join(random_line_orig))
    show_line_stats("".join(random_line_orig))

    # Wzorowy tekst
    print("Original line:")
    show_line_stats(line)

    gen_length = 200

    # Przybliżenie pierwszego rzędu 
    print("1st-order Markov approximation:")
    model_1 = build_markov_model(line, 1)
    random_line_1 = generate_markov_text(model_1, 1, gen_length)
    print("Generated line:", random_line_1)
    show_line_stats(random_line_1)

    # Przybliżenie trzeciego rzędu
    print("3rd-order Markov approximation:")
    model_3 = build_markov_model(line, 3)
    random_line_3 = generate_markov_text(model_3, 3, gen_length)
    print("Generated line:", random_line_3)
    show_line_stats(random_line_3)

    # Przybliżenie piątego rzędu startujące od 'probability'
    print("5th-order Markov approximation (start: 'probability'):")
    model_5 = build_markov_model(line, 5)
    random_line_5 = generate_markov_text(model_5, 5, gen_length, seed="probability")
    print("Generated line:", random_line_5)
    show_line_stats(random_line_5)

if __name__ == "__main__":
    main()