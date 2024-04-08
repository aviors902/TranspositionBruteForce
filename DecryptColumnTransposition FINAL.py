from itertools import permutations
import nltk
from nltk.corpus import words

def split_ciphertext(ciphertext, period):
    period = int(period)
    if len(ciphertext) % period != 0:
        diff = period - (len(ciphertext) % period)
        while diff != 0:
            ciphertext += "X"
            diff -= 1
    rows = []
    for i in range(0, len(ciphertext), period):
        row = ciphertext[i:i + period]
        rows.append(list(row))
    return rows

def all_permutations(period):
    permuted_lists = permutations(range(period))
    list_of_permutations = []
    for permuted_list in permuted_lists:
        list_of_permutations.append(permuted_list[:])
    return list_of_permutations

def decrypt_with_permutation(ciphertext, permutation):
    chunk_size = len(ciphertext) // len(permutation)
    columns = [''] * len(permutation)
    for i, idx in enumerate(permutation):
        start = idx * chunk_size
        end = start + chunk_size
        columns[i] = ciphertext[start:end]
    decrypted_text = ''.join([''.join(column) for column in zip(*columns)])
    return decrypted_text

def reverse_engineer_transposition(ciphertext, period):
    permutations_list = permutations(range(period))
    decrypted_texts = []
    corresponding_permutations = []
    for permutation in permutations_list:
        decrypted_text = decrypt_with_permutation(ciphertext, permutation)
        decrypted_texts.append(decrypted_text)
        corresponding_permutations.append(permutation)
    return corresponding_permutations, decrypted_texts

def find_english_words(text, min_word_length=3):
    nltk.download('words', quiet=True)
    english_words = set(words.words())
    found_words = []
    for i in range(len(text)):
        for j in range(i + min_word_length, len(text) + 1):
            word = text[i:j]
            if word.lower() in english_words:
                found_words.append(word)
    return found_words


def print_most_likely_options(most_likely_options):
    for idx, options in enumerate(most_likely_options, 1):
        print()
        print("**********************")
        print(f"Most likely column transpositions for Period {idx}:")
        print("**********************")
        print()
        for inner_idx, (option_number, joined_text, word_count, permutation_order, words_found, decrypted_text) in enumerate(options, 1):
            print(f"Option {inner_idx}: {joined_text}")  # Print the joined permutation
            print(f"Permutation Order: {permutation_order}")  # Print the permutation order
            print(f"English word count: {word_count}")
            print(f"Decrypted Text: {decrypted_text}")
            print()
        print()

def count_english_words_in_permutations(ciphertext, period, min_word_length=2):
    most_likely_options = []
    for idx in range(1, period + 1):
        permutations, decrypted_texts = reverse_engineer_transposition(ciphertext, idx)
        options = []
        for inner_idx, (permutation, decrypted_text) in enumerate(zip(permutations, decrypted_texts), 1):
            english_words = find_english_words(decrypted_text, min_word_length)
            word_count = len(english_words)
            joined_text = ''.join(str(num) for num in permutation)  # Convert integers to strings
            permutation_order = list(all_permutations(idx)[inner_idx - 1])
            options.append((inner_idx, joined_text, word_count, permutation_order, english_words, decrypted_text))
        options.sort(key=lambda x: x[2], reverse=True)
        top_options = options[:5]
        most_likely_options.append(top_options)
        print_most_likely_options(most_likely_options)  # Print top 5 options at the end of each period's iteration
    return most_likely_options

print("Enter Cipher Text: ")
ciphertext = input()
ciphertext = ciphertext.replace(" ", "")

print("Enter maximum period to calculate to: ")
period = int(input())

most_likely_options = count_english_words_in_permutations(ciphertext, period)
print("----------------------------------------")
print("Done!")
input()