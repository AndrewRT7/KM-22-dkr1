# Problem Set 2, hangman.py
# Name: Andrew Yavorskyi
# Collaborators: -
# Time spent: approximately 17 hours

# Hangman Game
# -----------------------------------
# Helper code

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    guessing_result: list (of letters), which have been guessed and are present in secret word
    returns: boolean, True if set of unique letters in guessing_result is equal to set of unique letters in secret_word;
      False otherwise
    '''
    guessing_result = []
    for i in set(letters_guessed):
        if i in set(secret_word):
            guessing_result = guessing_result + [i]
            continue
    if set(guessing_result) == set(secret_word):
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    res_list = []
    for i in list(secret_word):
        if i in letters_guessed:
            res_list = res_list + [i]
            continue
        else:
            res_list = res_list + ['_ ']
            continue
    return res_list



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    for i in all_letters:
        if i in str(letters_guessed):
            all_letters = all_letters.replace(i, '')
    return all_letters


def warnings_remaining(warnings):
    '''
    warnings: quantity of warnings left after player`s guessing
    returns: word "no" if no usable warnings left
    '''
    if warnings == -1:
        warnings = 'no'
    return warnings
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, function shows the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user starts with 6 guesses

    * Before each round, it is displayed to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * The message asks user to supply one guess per round. The user will get feedback about
      his/her guess, whether it is valid or not
    
    * The user receives feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, function displays to the user the 
      partially guessed word.
    '''
    print('Welcome to the game Hangman!\nI am thinking of a word that is', len(secret_word), 'letters long.')
    attempts = 6
    warnings = 3
    vowel = ['a', 'e', 'u', 'i', 'o']
    letters_guessed = []
    while True:
        if is_word_guessed(secret_word, letters_guessed) == True:
            return print(f'{"-"*25}\nCongratulations, you`ve won!\nYour total score for this game is:', attempts * len(set(secret_word)))
        elif attempts <= 0 and is_word_guessed(secret_word, letters_guessed) == False:
            return print(f'{"-"*25}\nSorry, you ran out of guesses. The word was:', secret_word)
        else:
            if warnings_remaining(warnings) == 'no':
                attempts -= 1
                warnings += 1
            print(f'{"-"*25}\nYou have', attempts, 'attempts left.\nAvailable letters:', get_available_letters(letters_guessed))
            guess = (input('Please take a guess (it should be only one letter): ')).lower()
            if guess.isalpha() and len(list(guess)) == 1 and (guess in letters_guessed) == False:
                letters_guessed = letters_guessed + [guess]
                if guess in list(secret_word):
                    print('You`re right: ', *get_guessed_word(secret_word, letters_guessed))
                elif (guess in list(secret_word)) == False and guess in vowel:
                    print('Unfortunately, you`re wrong: ', *get_guessed_word(secret_word, letters_guessed))
                    attempts -= 2
                elif (guess in list(secret_word)) == False and (guess in vowel) == False:
                    print('Unfortunately, you`re wrong: ', *get_guessed_word(secret_word, letters_guessed))
                    attempts -= 1 
            elif guess.isalpha() == False:
                warnings -= 1
                print('You need to type in a letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))
            elif len(list(guess)) != 1:
                warnings -= 1
                print('You need to type in only one letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))
            elif guess in letters_guessed:
                warnings -= 1
                print('You already guessed that letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))



# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(list(my_word.replace(' ', ''))) == len(list(other_word)):
        my_list = list((my_word.replace(' ', '')))
        other_list = list(other_word)
        for i in range(len(my_list)):
            if (my_list[i]) == '_':
                (other_list[i]) = '_'
        if my_list == other_list:
            return True 
        else:
            return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    for i in wordlist:
        if match_with_gaps(my_word, i) == True:
            print(i, end = '; ')
        elif i == '':
            print('No matches found')
    return ''


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print('Welcome to the game Hangman!\nI am thinking of a word that is', len(secret_word), 'letters long.')
    attempts = 6
    warnings = 3
    vowel = ['a', 'e', 'u', 'i', 'o']
    letters_guessed = []
    while True:
        if is_word_guessed(secret_word, letters_guessed) == True:
            return print(f'{"-"*25}\nCongratulations, you`ve won!\nYour total score for this game is:', attempts * len(set(secret_word)))
        elif attempts <= 0 and is_word_guessed(secret_word, letters_guessed) == False:
            return print(f'{"-"*25}\nSorry, you ran out of guesses. The word was:', secret_word)
        else:
            if warnings_remaining(warnings) == 'no':
                attempts -= 1
                warnings += 1
            print(f'{"-"*25}\nYou have', attempts, 'attempts left.\nAvailable letters:', get_available_letters(letters_guessed))
            guess = (input('Please take a guess (it should be only one letter): ')).lower()
            if guess.isalpha() and len(list(guess)) == 1 and (guess in letters_guessed) == False:
                letters_guessed = letters_guessed + [guess]
                if guess in list(secret_word):
                    print('You`re right: ', *get_guessed_word(secret_word, letters_guessed))
                elif (guess in list(secret_word)) == False and guess in vowel:
                    print('Unfortunately, you`re wrong: ', *get_guessed_word(secret_word, letters_guessed))
                    attempts -= 2
                elif (guess in list(secret_word)) == False and (guess in vowel) == False:
                    print('Unfortunately, you`re wrong: ', *get_guessed_word(secret_word, letters_guessed))
                    attempts -= 1 
            elif guess.isalpha() == False and guess != '*':
                warnings -= 1
                print('You need to type in a letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))
            elif len(list(guess)) != 1:
                warnings -= 1
                print('You need to type in only one letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))
            elif guess in letters_guessed:
                warnings -= 1
                print('You already guessed that letter. You have', warnings_remaining(warnings), 'warnings left:', *get_guessed_word(secret_word, letters_guessed))
            elif guess == '*':
                print('Possible word matches are: ')
                print(show_possible_matches((get_guessed_word(secret_word, letters_guessed)))) 


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.



if __name__ == "__main__":
    #pass

    #To test part 2, comment out the pass line above and
    #uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
