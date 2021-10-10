import urllib.request
from collections import OrderedDict
import random

# Getting the txt file of the novel 
text = open("Sherlock.txt", encoding='utf-8')
cleaned_text_words = []
# Removing \r and \n in every line that is parsed
# Also removing any occurences of spaces and empty words  
for line in text:
    line = line.replace('\r', ' ')
    line = line.replace('\n', ' ')
    line = line.encode('ascii', errors= 'ignore')
    words = line.decode().split(' ')
    word = words[1]
    updated_words = [word for word in words if word not in ['', ' ']]
    cleaned_text_words += updated_words
print('Length of the corpus: {0}'.format((len(cleaned_text_words))))
# Dictionary is the list of unique words that make up the corpus
dictionary = list(OrderedDict.fromkeys(cleaned_text_words))
print('Length of the dictionary: {0}'.format((len(dictionary))))

# 1) A transition map holds a 3 consecutive words as its key and a list of next words that occur after the key in the corpus
# 2) Duplicate entries in the map are left unremoved because this will increase the probability that the frequently
#    occuring word combinations will be picked 
transition_map = {}
for pos, word in enumerate(cleaned_text_words):
    if pos <= len(cleaned_text_words)-5:
        word2 = cleaned_text_words[pos+1]
        word3 = cleaned_text_words[pos+2]
        if (word, word2) in transition_map:
            transition_map[(word, word2)].append(word3)
        else:
            transition_map[(word, word2)] = [word3]

def generate_text(transition_map, no_of_words, seed1, seed2):
    generated_text = [seed1, seed2]
    curr_word1 = seed1
    curr_word2 = seed2
    for i in range(no_of_words-3):
        next_word = random.choice(transition_map[(curr_word1, curr_word2)])
        generated_text.append(next_word)
        curr_word1 = curr_word2
        curr_word2 = next_word
    return generated_text

# 2 consecutive words at random from the corpus are picked as the seeding words
choice = random.randint(0, len(cleaned_text_words)-1)
seed1 = cleaned_text_words[choice]
seed2 = cleaned_text_words[choice+1]
no_of_words = 50
result = generate_text(transition_map, no_of_words, seed1, seed2)
# Unpacking the list 
print("Generated text: ", *result)