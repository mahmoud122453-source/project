import string

def get_words(filename):
    try:
        with open(filename, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("file is not exist buddy")
        return None
    
    for char in string.punctuation:
        text = text.replace(char, '')

    words = text.lower().split()
    return words

def count_words(words):
    counts = {}

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def display_top(counts, top_n=5):
    sorted_words = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\nTop {top_n} most frequent words:\n")
    for word, count in sorted_words[:top_n]:
        print(f"  {word:>20} {count}")

def main():
    filename = input("Enter text file name: ")
    words = get_words(filename)
    if words is None:
        return
    counts = count_words(words)
    display_top(counts)

if __name__ == "__main__":
    main()



 
