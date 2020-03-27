import csv
import re
import string
import random

MIN_WORD_COUNT = 3

def choose_weighted(d):
    choices = []
    for k, v in d.items():
        choices.extend([k] * (v**2))
    return random.choice(choices)

def build_sentence(chains, start_word, length):
    words = [start_word]
    
    def get_key(l):
        m = l if l < len(chains) else len(chains)
        return tuple(words[-m:])

    while len(words) < length:
        chain_idx = len(words) - 1 if len(words) - 1 < len(chains) - 1 else len(chains) - 1
        print('chain idx:', chain_idx)
        key = get_key(len(words))
        while key not in chains[chain_idx]:
            chain_idx -= 1
            key = key[:-1]
        next_word = choose_weighted(chains[chain_idx][key])
        print('key len:', len(key),'key:', key)
        print('next word:', next_word)
        words.append(next_word)
        print(words)
        print('-'*20)

    return ' '.join(words).capitalize()

chains = []
sentences = []

max_i = 10000000
i = 0

# Open the file
with open('trumptweets.csv', 'r') as f:
    # Parse the csv
    reader = csv.reader(f)

    # TODO: Skip over the first row cuz its just headers
    # Iterate over each tweet
    for row in reader:
        if i > max_i:
            break

        # Lower case everything so we dont have to worry about case sensitivity later
        content = row[2].lower()

        # Remove urls (assuming a blah.tld as a pattern)
        content = re.sub(r"\b\S*\.\S+", '', content)

        # Remove quotes
        content = re.sub(r'".*"', '', content)

        # Remove mentions
        content = re.sub(r'@\S*', '', content)

        # Make a clean copy with only ascii chars
        clean = ''
        for c in content:
            if c in string.ascii_lowercase+" \n'":
                clean += c
            else:
                clean += ' '
        content = clean

        # Since we want coherent word strings, we want sentences so lets split by '.'
        # The list comp is to remove empty strings and check for word counts
        s = [_ for _ in content.split('.') if _ and len(_.split()) >= MIN_WORD_COUNT]

        # Add the result to our collection
        sentences.extend(s)

        i += 1

print('Using', len(sentences), 'sentences')

max_chunk_size = 3
# Build the chains
for chunk_idx in range(max_chunk_size):
    chain = {}
    chains.append(chain)
    chunk_size = chunk_idx + 1
    for sentence in sentences:
        words = sentence.split()
        i = 0
        while i < len(words) - chunk_size:
            word = tuple(words[i:i+chunk_size])
            next_word = words[i+chunk_size]
            if word in chain:
                if next_word in chain[word]:
                    chain[word][next_word] += 1
                else:
                    chain[word][next_word] = 1
            else:
                chain[word] = {next_word: 1}
            i += 1

print('Chain complete')
