import random


def get_char_freqs(text, out_len, limit=27):
    text = text[:limit]
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1

    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    probs = {k: v / len(text) for k, v in sorted_counts.items()}

    result = random.choices(
        list(probs.keys()),
        list(probs.values()),
        k=out_len
    )
    return "".join(result)


def print_text_info(text):
    words = text.split()
    if not words:
        return
    w_count = len(words)
    total_chars = sum(len(w) for w in words)

    print(f"Words count: {w_count}")
    print(f"Total chars in words: {total_chars}")
    print(f"Avg word length: {round(total_chars / w_count, 2)}\n")


def make_model(data, step):
    m = {}
    for i in range(len(data) - step):
        chunk = data[i:i + step]
        nxt = data[i + step]
        if chunk not in m:
            m[chunk] = []
        m[chunk].append(nxt)
    return m


def run_markov(m, step, length, start_word=None):
    if start_word is None:
        current = random.choice(list(m.keys()))
        out_text = current
    else:
        out_text = start_word

    while len(out_text) < length:
        tail = out_text[-step:]
        if tail in m:
            out_text += random.choice(m[tail])
        else:
            out_text += random.choice(list(m.keys()))

    return out_text[:length]


def run():
    print("--- Level 0 ---")
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    t0 = get_char_freqs(alphabet, 50)
    print("Output:", t0)
    print_text_info(t0)

    try:
        with open("data/norm_wiki_sample.txt", "r", encoding="utf-8") as file:
            source_data = file.read()[:50000]
    except FileNotFoundError:
        print("Error: File not found.")
        return

    print("--- Loaded text stats ---")
    t1 = get_char_freqs(source_data, 50, 20000)
    print("Output:", t1)
    print_text_info(t1)

    print("--- Markov level 1 ---")
    mod1 = make_model(source_data, 1)
    res1 = run_markov(mod1, 1, 200)
    print("Output:", res1)
    print_text_info(res1)

    print("--- Markov level 3 ---")
    mod3 = make_model(source_data, 3)
    res3 = run_markov(mod3, 3, 200)
    print("Output:", res3)
    print_text_info(res3)

    print("--- Markov level 5 (start word) ---")
    mod5 = make_model(source_data, 5)
    res5 = run_markov(mod5, 5, 200, start_word="probability")
    print("Output:", res5)
    print_text_info(res5)


if __name__ == "__main__":
    run()