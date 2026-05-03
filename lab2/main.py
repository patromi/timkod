import random

def generate_line(base_string, length):
    generated_line = random.choices(list(base_string.keys()), weights=list(base_string.values()), k=length)
    gstring = " ".join(generated_line)
    return gstring

def generate_markov_1st_order(chain, start_word, length):
    result = [start_word]
    current_word = start_word
    
    for _ in range(length - 1):
        if current_word not in chain:
            break
            
        next_words = list(chain[current_word].keys())
        weights = list(chain[current_word].values())
        
        chosen_word = random.choices(next_words, weights=weights, k=1)[0]
        result.append(chosen_word)
        
        current_word = chosen_word
            
    return " ".join(result)

def generate_markov_2nd_order(chain, start_tuple, length):
    result = list(start_tuple)
    current_state = start_tuple
    
    for _ in range(length - 2):
        if current_state not in chain:
            break
            
        next_words = list(chain[current_state].keys())
        weights = list(chain[current_state].values())
        
        chosen_word = random.choices(next_words, weights=weights, k=1)[0]
        result.append(chosen_word)
        
        current_state = (current_state[1], chosen_word)
            
    return " ".join(result)




if __name__ == "__main__":
     
    with open("data/norm_wiki_sample.txt", "r", encoding="utf-8") as f:
            line = f.read().split()[:50000]

    total_words = len(line)

    word_counts = {}
    for word in line:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    top_10 = sorted_word_counts[:10]

    print("Najczęściej występujące słowa:")
    for word, count in top_10:
        percentage = (count / total_words) * 100
        print(f"Słowo '{word}': {count}/{total_words} ({percentage:.2f}%)")

    print("\nFirst order approximation:")
    print(generate_line(word_counts, 30))


    markov_1 = {}
    for i in range(len(line) - 1):
        state = line[i]
        next_word = line[i+1]
        
        if state not in markov_1:
            markov_1[state] = {}
        markov_1[state][next_word] = markov_1[state].get(next_word, 0) + 1

    print("\n Markow 1. rzędu")
    start_word_1 = line[0] 
    print(generate_markov_1st_order(markov_1, start_word_1, 30))


    markov_2 = {}
    for i in range(len(line) - 2):
        state = (line[i], line[i+1])
        next_word = line[i+2]
        
        if state not in markov_2:
            markov_2[state] = {}
        markov_2[state][next_word] = markov_2[state].get(next_word, 0) + 1

    print("\nMarkow 2. rzędu")
    start_state_2 = (line[0], line[1])
    print(generate_markov_2nd_order(markov_2, start_state_2, 30))


    print("\nMarkow 2. rzędu (start: 'probability')")
    word1 = "probability"
    
    if word1 in markov_1:
        next_words = list(markov_1[word1].keys())
        weights = list(markov_1[word1].values())
        word2 = random.choices(next_words, weights=weights, k=1)[0]
        
        start_state_prob = (word1, word2)
        print(generate_markov_2nd_order(markov_2, start_state_prob, 30))
    else:
        print(f"Słowo '{word1}' nie występuje w tekście.")