# This is a script to generate all possible permutations of a collumn transpostition cipher for a given period d in the user's input ciphertext
# The script will return the top 5 most likely results based on the count of english words present in the permuted ciphertext
from itertools import permutations
import nltk
from nltk.corpus import words


def split_ciphertext(ciphertext, period):
    period = int(period)
    ciphertext = ciphertext.replace(" ", "")
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

#Calculate evry single posible collumnar permutation for the given period
def all_permutations(period):
    # Generate all permutations of integers from 0 to period-1
    permuted_lists = permutations(range(period))
    # Convert each permutation into a list of integers
    list_of_permutations = []
    for permuted_list in permuted_lists:
        list_of_permutations.append(permuted_list[:])
        #print(permuted_list) - Used for debugging
    return list_of_permutations


def permute_ciphertext(ciphertext, period):
    # Split the ciphertext into rows with the given period
    rows = split_ciphertext(ciphertext, period)
    # Generate all possible permutations for the given period
    permutation_list = all_permutations(period)
    # Initialize the result list
    result = []
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
        # Append the joined rows to the result list
        result.append(joined_rows)
    return result

def transpose_columns_to_rows(result):
    # Transpose columns back to rows
    transposed_rows = [''.join(column) for column in zip(*result)]
    return transposed_rows

def generate_original_possibilities(ciphertext, result):
    possibilities = []
    for arrangement in result:
        # Transpose columns back to rows
        transposed_rows = transpose_columns_to_rows(arrangement)
        # Concatenate the rows to get the original plaintext without spaces
        original_plaintext = ''.join(transposed_rows)
        possibilities.append(original_plaintext)
    return possibilities

def find_english_words(text, min_word_length=3):
    nltk.download('words', quiet=True)
    english_words = set(words.words())
    found_words = []
    for i in range(len(text)):
        for j in range(i + min_word_length, len(text) + 1):
            word = text[i:j]
            if word.lower() in english_words and len(word) >= min_word_length:
                found_words.append(word)
    return found_words

def count_english_words_in_permutations(ciphertext, period, min_word_length=3):
    permutations = permute_ciphertext(ciphertext, period)
    top_options = []
    for idx, permutation in enumerate(permutations):
        transposed_rows = transpose_columns_to_rows(permutation)
        text = ''.join(transposed_rows)
        english_words = find_english_words(text, min_word_length)
        unique_english_words = set(english_words)  # Convert to set to remove duplicates
        word_count = len(unique_english_words)  # Count unique words only
        joined_text = ''.join(transposed_rows)
        top_options.append((joined_text, word_count, permutation))
    top_options.sort(key=lambda x: x[1], reverse=True)
    return top_options[:5]

def print_top_options(top_options, column_permutations):
    print("Top 5 Options based on English word count:")
    for idx, (option, word_count, arrangement) in enumerate(top_options):
        joined_option = option.replace('X', '')
        # Retrieve the column position index numbers
        column_order = column_permutations[idx]
        print(f"Option {idx + 1}: {joined_option} (Column Order: {column_order})")
        print(f"English word count: {word_count}")
        # Find English words in the option
        english_words = find_english_words(joined_option)
        print("English words found:", english_words)
        print()

print("Enter Ciphertext: ")
ciphertext = input()
print("Enter period")
period = int(input())
print("Enter Minimum word length: ")
min_word_length = int(input())

print("Processing Please wait....")
#Calculates all possible permutations of the ciphertext and all possible row permutations for "Period" number of rows
column_permutations = all_permutations(period)

# Calculate top_options before calling print_top_options_with_column_order
top_options = count_english_words_in_permutations(ciphertext, period, min_word_length)
#print(permute_ciphertext(ciphertext, period))
print("-----------------------")

print_top_options(top_options, column_permutations)

print("-----------------------")