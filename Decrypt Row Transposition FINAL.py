from itertools import permutations
import nltk
from nltk.corpus import words


def split_ciphertext(ciphertext, period):
    period = int(period)
    ciphertext = ciphertext.replace(" ", "")
    if len(ciphertext) % period != 0:
        diff = period - (len(ciphertext) % period)
        while diff != 0:
            ciphertext += "-"
            diff -= 1

    rows = []
    for i in range(0, len(ciphertext), period):
        row = ciphertext[i:i + period]
        rows.append(list(row))
    return rows

# Calculate every single possible columnar permutation for the given period
def all_permutations(period):
    # Generate all permutations of integers from 0 to period-1
    permuted_lists = permutations(range(period))
    # Convert each permutation into a list of integers
    list_of_permutations = []
    for permuted_list in permuted_lists:
        list_of_permutations.append(permuted_list[:])
    return list_of_permutations


def permute_ciphertext(ciphertext, period):
    # Split the ciphertext into rows with the given period
    rows = split_ciphertext(ciphertext, period)
    # Generate all possible permutations for the given period
    permutation_list = all_permutations(period)
    # Initialize the ciphertext_permutations list
    ciphertext_permutations = []
    # Iterate over each permutation in the permutation list
    for perm in permutation_list:
        # Create a new list to hold the rearranged columns
        rearranged_columns = []
        # Iterate over each index in the permutation
        for idx in perm:
            # Create a new column by selecting the character at the index from each row
            new_row = []
            for row in rows:
                new_row.append(row[idx])
            # Append the column to the rearranged columns list
            rearranged_columns.append(new_row[:])
        # Join each row
        joined_rows = [''.join(row) for row in rearranged_columns]
        # Append the joined rows to the ciphertext_permutations list
        ciphertext_permutations.append(joined_rows)
    return ciphertext_permutations

def transpose_columns_to_rows(ciphertext_permutations):
    # Transpose columns back to rows
    transposed_rows = [''.join(column) for column in zip(*ciphertext_permutations)]
    return transposed_rows

def generate_original_possibilities(ciphertext, ciphertext_permutations):
    possibilities = []
    for arrangement in ciphertext_permutations:
        # Transpose columns back to rows
        transposed_rows = transpose_columns_to_rows(arrangement)
        # Concatenate the rows to get the original plaintext without spaces
        original_plaintext = ''.join(transposed_rows)
        possibilities.append(original_plaintext)
    return possibilities

def find_english_words(text, min_word_length=1):
    nltk.download('words', quiet=True)
    english_words = set(words.words())
    found_words = []
    for i in range(len(text)):
        for j in range(i + min_word_length, len(text) + 1):
            word = text[i:j]
            if word.lower() in english_words:
                found_words.append(word)
    return found_words

def count_english_words_in_permutations(ciphertext, period, min_word_length=2):
    permutations = permute_ciphertext(ciphertext, period)
    top_options = []  # List to store the top options
    for idx, permutation in enumerate(permutations):
        transposed_rows = transpose_columns_to_rows(permutation)
        text = ''.join(transposed_rows)
        english_words = find_english_words(text, min_word_length)
        word_count = len(english_words)
        joined_text = ''.join(transposed_rows)  # Join the permutation into one long string
        top_options.append((idx + 1, joined_text, word_count, english_words))  # Append tuple of permutation number, joined permutation, word count, and words found
    top_options.sort(key=lambda x: x[2], reverse=True)  # Sort options by word count in descending order
    return top_options[:5]  # Return only top 5 options

print("-----------------------")
print("Input Ciphertext here: ")
ciphertext = input()
print("-----------------------")
print("Input maximum period to calculate to:")
period = int(input())

print("Minimum word length (Number of characters): ")
min_word_length = int(input())

print("Procecssing... Please wait...")
print("-----------------------")
ciphertext_permutations = permute_ciphertext(ciphertext, period)
permutation_options = all_permutations(period)
#print(ciphertext_permutations)
'''
print("All Possibilities based on Permutations:")
original_possibilities = generate_original_possibilities(ciphertext, ciphertext_permutations)
for idx, possibility in enumerate(original_possibilities):
    print(f"Option {idx + 1}: {possibility}")
'''


top_options = count_english_words_in_permutations(ciphertext, period, min_word_length)
print("-----------------------")
print("Top 5 Options based on English word count:")
print("-----------------------")
for idx, (option_number, option, word_count, words_found) in enumerate(top_options):
    print(f"Option {option_number}: {option.replace('-', '')}")  # Print the joined permutation without 'X' separators
    print("Permutation Order: ", permutation_options[option_number-1] )
    print(f"English word count: {word_count}")
    print(f"English words found: {words_found}")
    print()

print("-----------------------")
print("Done!")
input()
