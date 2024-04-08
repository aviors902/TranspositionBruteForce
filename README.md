# TranspositionBruteForce
Scrpits that can be used to brute force row or transposition cipher
Written in python, the following dependancies are required
  - itertools (Iterative tools, used to generate all the possible transposition permutations)
  - nltk (Natural Language Toolkit - Used to recognise sequential characters as real english words when counting the words present in an individual ciphertext permutation. Can be a bit janky sometimes, recommended not having minimum word size be less than 3)


Assumptions made are:
  - Plaintext was encrypted with 1 set of transpositions
  - Row transposition cipher plainexts were written in columns
  - Column transposition cipher plaintexts were written in rows
