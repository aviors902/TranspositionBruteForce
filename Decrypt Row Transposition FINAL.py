from itertools import permutations
import nltk
from nltk.corpus import words

# Splits the ciphertext into the columns that would exist when using "Period" number of rows. Strips any spaces in the text and also appends an X to the end of the text to ensure it'll perfectly fill the rows
def split_ciphertext(ciphertext, period):
    period = int(period)
    ciphertext = ciphertext.replace(" ", "")
    if len(ciphertext) % period != 0:                                            # Checking to see if the ciphertext needs to be bulked out to fit the columns
        diff = period - (len(ciphertext) % period)
        while diff != 0:                                        # Bulks out the text with appropriate number of X's
            ciphertext += "X"
            diff -= 1

    rows = []
    for i in range(0, len(ciphertext), period):
        row = ciphertext[i:i + period]
        rows.append(list(row))
    return rows                                                 # Returns a 2d array, where each row in the array is a row from the ciphertext

# Calculate every single possible columnar permutation for the given period
def all_permutations(period):
    # Generate all permutations of integers from 0 to period-1
    permuted_lists = permutations(range(period))
    # Convert each permutation into a list of integers
    list_of_permutations = []
    for permuted_list in permuted_lists:
        list_of_permutations.append(permuted_list[:])
    return list_of_permutations                                  # Returns a 2d array, basically a list of every possible order that the rows could be taken    

# Generates every possible permutation of the ciphertext based on the permutation orders returned by all_permutations()
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
    return ciphertext_permutations                              # Returns a list of 2d lists, each 2d list is a list of all row permutations for the period that can be applied to the ciphertext

# Takes all the 2d matrix and changes the orientation so that each new "Column" (Previously was a row) is able to be joined into one long string for readability and word counting
def transpose_columns_to_rows(ciphertext_permutations):
    # Transpose columns back to rows
    transposed_rows = [''.join(column) for column in zip(*ciphertext_permutations)]
    return transposed_rows                                      # Returns a string which is the plaintext generated from the argument passed

# Takes the permuted ciphertext stored in result, transposes each of the permutations with transpose_columns_to_rows so that they can be tested for English words
def generate_original_possibilities(ciphertext, ciphertext_permutations):
    possibilities = []
    for arrangement in ciphertext_permutations:
        # Transpose columns back to rows
        transposed_rows = transpose_columns_to_rows(arrangement)
        # Concatenate the rows to get the original plaintext without spaces
        original_plaintext = ''.join(transposed_rows)
        possibilities.append(original_plaintext)
    return possibilities                                        # Returns the list of plaintexts generated

# Checks a given plaintext for english words and returns the number of english words found. Default minimum wordlength is 3 but can be changed by user input
def find_english_words(text, min_word_length=1):
    nltk.download('words', quiet=True)
    english_words = set(words.words())
    found_words = []
    for i in range(len(text)):
        for j in range(i + min_word_length, len(text) + 1):
            word = text[i:j]
            if word.lower() in english_words:
                found_words.append(word)
    return found_words                                          # Returns the list of english words that have been found in the plaintext. Can sometimes contain double-ups and if the minimum is set below 3 it will also return random non-english 2-character "Words"

# Uses the find_english_words() function to iterate every single plaintext generated and then return the 5 with the highest wordcount
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
    return top_options[:5]                                      # Returns the 5 plaintexts with the highest wordcounts, the permutation order and the wordcount. Changing this return will increase or decrease the number of string results returned


# Main function, calls the above functions in order of their requirement.
# 1. Split the ciphertext into period number of columns
# 2. Calculate all possible permutations of the numbers 1 to period
# 3. Re-order the ciphertext according to each of the calculated permutations
# 4. Transpose the columns into rows (So that rather than being a vertical column, the column can be read left to right)
# 5. Concatonate each of the sets rows to create a set of plaintexts
# 6. Count the number of english words in each plaintext and record the number
# 7. Order the list from highest number of English words to lowest and print the top 5
# 8. Start again, increasing the number of collumns included in the calculations by 1
# 9. Repeat until the user specified period has been calculated.
def main():
    print("-----------------------")
    print("Input Ciphertext here: ")
    ciphertext = input()
    print("-----------------------")
    print("Input maximum period to calculate to:")
    max_period = int(input())
    print("Minimum word length (Number of characters): ")
    min_word_length = int(input())
    print("Procecssing... Please wait...")
    print("-----------------------")
    for period in range(1, max_period + 1):
        permutation_options = all_permutations(period)
        top_options = count_english_words_in_permutations(ciphertext, period, min_word_length)
        print("-----------------------")
        print(f"Top 5 Options for Period {period} based on English word count:")
        print("-----------------------")
        for idx, (option_number, option, word_count, words_found) in enumerate(top_options):
            print(f"Option {option_number}: {option.replace('X', '')}")  # Print the joined permutation without 'X' separators
            print("Permutation Order: ", permutation_options[option_number - 1])
            print(f"English word count: {word_count}")
            # print(f"English words found: {words_found}")               #Uncomment if you want a list of every word found. Mainly used for debugging
            print()
    print("-----------------------")
    print("Done! Press enter to exit")
    input()

if __name__ == "__main__":
    main()
