# This is a script to generate all possible permutations of a collumn transpostition cipher for a given period d in the user's input ciphertext
# The script will return the top 5 most likely results based on the count of english words present in the permuted ciphertext
from itertools import permutations
import nltk
from nltk.corpus import words

# Splits the ciphertext into the columns that would exist when using "Period" number of rows. Strips any spaces in the text and also appends an X to the end of the text to ensure it'll perfectly fill the rows
def split_ciphertext(ciphertext, period):
    period = int(period)
    ciphertext = ciphertext.replace(" ", "")
    if len(ciphertext) % period != 0:                           # Checking to see if the ciphertext needs to be bulked out to fit the columns
        diff = period - (len(ciphertext) % period)
        while diff != 0:                                        # Bulks out the text with appropriate number of X's
            ciphertext += "X"
            diff -= 1
    rows = []
    for i in range(0, len(ciphertext), period):
        row = ciphertext[i:i + period]
        rows.append(list(row))
    return rows                                                 # Returns a 2d array, where each row in the array is a row from the ciphertext

# Calculates evry single posible collumnar permutation for the given period
def all_permutations(period):
    # Generate all permutations of integers from 0 to period-1
    permuted_lists = permutations(range(period))
    # Convert each permutation into a list of integers
    list_of_permutations = []
    for permuted_list in permuted_lists:
        list_of_permutations.append(permuted_list[:])
        #print(permuted_list) - Used for debugging
    return list_of_permutations                                 # Returns a 2d array, basically a list of every possible order that the rows could be taken

# Generates every possible permutation of the ciphertext based on the permutation orders returned by all_permutations()
def permute_ciphertext(ciphertext, period):
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
            # Create a new list by adding the idx-th character at the index from each row (Basically permuting the row position in every column)
            new_row = []
            for row in rows:
                new_row.append(row[idx])
            # Append the row to the rearranged row list
            rearranged_columns.append(new_row[:])
        # Join each row so it is not a list of lists of lists
        joined_rows = [''.join(row) for row in rearranged_columns]
        # Append the joined rows to the result list
        result.append(joined_rows)
    return result                                               # Returns a list of 2d lists, each 2d list is a list of all row permutations for the period that can be applied to the ciphertext

# Takes all the 2d matrix and changes the orientation so that each new "Column" (Previously was a row) is able to be joined into one long string for readability and word counting
def transpose_columns_to_rows(result):
    # Transpose columns back to rows
    transposed_rows = [''.join(column) for column in zip(*result)]
    return transposed_rows                                      # Returns a string which is the plaintext generated from the argument passed

# Takes the permuted ciphertext stored in result, transposes each of the permutations with transpose_columns_to_rows so that they can be tested for English words
def generate_original_possibilities(result):
    possibilities = []
    for arrangement in result:
        # Transpose columns back to rows
        transposed_rows = transpose_columns_to_rows(arrangement)
        # Concatenate the rows to get the original plaintext without spaces
        original_plaintext = ''.join(transposed_rows)
        possibilities.append(original_plaintext)
    return possibilities                                        # Returns the list of plaintexts generated

# Checks a given plaintext for english words and returns the number of english words found. Default minimum wordlength is 3 but can be changed by user input
def find_english_words(text, min_word_length=3):
    nltk.download('words', quiet=True)
    english_words = set(words.words())
    found_words = []
    for i in range(len(text)):
        for j in range(i + min_word_length, len(text) + 1):
            word = text[i:j]
            if word.lower() in english_words and len(word) >= min_word_length:
                found_words.append(word)
    return found_words                                          # Returns the list of english words that have been found in the plaintext. Can sometimes contain double-ups and if the minimum is set below 3 it will also return random non-english 2-character "Words"

# Uses the find_english_words() function to iterate every single plaintext generated and then return the 5 with the highest wordcount
def count_english_words_in_permutations(ciphertext, period, min_word_length=3):
    permutations = permute_ciphertext(ciphertext, period)
    top_options = []
    for idx, permutation in enumerate(permutations):
        transposed_rows = transpose_columns_to_rows(permutation)
        # Joins the rows into one single string so the words can be searched
        text = ''.join(transposed_rows)
        english_words = find_english_words(text, min_word_length)
        unique_english_words = set(english_words)  # Convert to set to remove duplicates
        word_count = len(unique_english_words)  # Count unique words only
        joined_text = ''.join(transposed_rows)
        top_options.append((joined_text, word_count, permutation))
    top_options.sort(key=lambda x: x[1], reverse=True)
    return top_options[:5]                                      # Returns the 5 plaintexts with the highest wordcounts, the permutation order and the wordcount. Changing this return will increase or decrease the number of string results returned


# Function used to print the options obtained when running count_english_words_in_permutation() and format the output nicely
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

def main():
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
    print("Press enter to exit.")
    input()

if __name__ == "__main__":
    main()
