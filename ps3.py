import os
import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


def get_word_score(word, n):
    word = word.lower()
    Component1 = 0
    for x in word:
        lettervalue = SCRABBLE_LETTER_VALUES[x]
        Component1 = Component1 + lettervalue
    if 7*len(word)-3*(n-len(word))<1:
        Component2 = 1
    else:
        Component2 = 7*len(word)-3*(n-len(word))
    wordscore = Component1 * Component2
    return wordscore

def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      
    print()                              

def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    x = "*"
    hand[x] = hand.get(x,0) + 1

    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

def match_word(word, other_word):
    word = word.lower()
    if len(word) != len(other_word):
        return False
    for i in range(0, len(other_word)):
        if str.isalpha(word[i]):
            if other_word[i] != word[i]:
                return False
        else:
            if not other_word[i] in VOWELS:
                return False
    return True

def update_hand(hand, word):
    hand_copy = []
    dict_hand = {}
    for letter in hand.keys():
        for j in range(hand[letter]):
            hand_copy.append(letter)
    for x in word.lower():
        if x in hand_copy:
            hand_copy.remove(x)
    for x in hand_copy:
        letter_count = hand_copy.count(x)
        dict_hand.update({x: letter_count})
    return dict_hand
def is_valid_word(word, hand, word_list):
    word = word.lower()
    hand_copy = []
    possible_words = []
    for y in hand.keys():
        for x in range(hand[y]):
            hand_copy.append(y)
    for x in word_list:
        if match_word(word, x):
            possible_words.append(x)
    if len(possible_words) == 0:
        return False
    for letter in word:
        hand_count = hand_copy.count(letter)
        word_count = word.count(letter)
        if not hand_count:
            hand_count = 0
        if word_count > hand_count:
            if letter == "*":
                if "*" in hand:
                    hand_copy.remove("*")
                else:
                    return False
            else:
                return False
    return True

def calculate_handlen(hand):
    hand_copy = []
    for y in hand.keys():
        for x in range(hand[y]):
            hand_copy.append(y)
    return len(hand_copy)

def play_hand(hand, word_list):
    total_score = 0
    while len(hand) > 0:
        display_hand(hand)
        word = input("Enter word, or !! to indicate that you are finished:")
        if word == "!!":
            break
        else:
            if is_valid_word(word, hand, word_list):
                total_score += get_word_score(word,len(hand))
                print(word,"earned",get_word_score(word,len(hand)),"points. Total: ",total_score)
            else:
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)

    if len(hand) > 0:
        print("Total score:", total_score)
    else:
        print("Ran out of letters. Total score:", total_score)    
    return total_score


def substitute_hand(hand, letter):
    
    if letter in hand:
        choices = []
        for x in VOWELS:
            if not x in hand:
                choices.append(x)
        for x in CONSONANTS:
            if not x in hand:
                choices.append(x)
        hand[random.choice(choices)] = hand.pop(letter)
        return hand
    
def play_game(word_list):
    number_of_hands = int(input("Enter total number of hands:"))
    overall_score = 0
    times_run = 0
    replay_times = 0
    while times_run < number_of_hands:
        hand = deal_hand(HAND_SIZE)
        display_hand(hand)
        substitution = input("Would you like to substitute a letter?")
        if substitution.lower() == "yes":
            letter = input("Which letter would you like to replace:")
            hand = substitute_hand(hand, letter)
        score = play_hand(hand, word_list)
        print("----------")
        if replay_times == 0:  
            replay = input("Would you like to replay the hand?")
            if replay.lower() == "yes":
                replay_times += 1
                score2 = play_hand(hand, word_list)
                print("----------")
                if score2 > score:
                    overall_score += score2
                else:
                    overall_score += score        
            else:
                overall_score += score
        else:
            overall_score += score
        times_run += 1
    print("Total score over all hands:", overall_score)
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
