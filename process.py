import random
import unicodedata

def generate_word(database):
    return random.sample(database,1)[0]
    # return 'sagui'

def normalize_word(word):
    return ''.join(ch for ch in unicodedata.normalize('NFKD', word.upper()) if not unicodedata.combining(ch))

def in_database(word, database):
    word = normalize_word(word)
    database = map(lambda word:normalize_word(word), database)

    return word in database

def guess(string, reference):
    string = normalize_word(string)
    reference = normalize_word(reference)
    
    result = []
    for i in range(len(reference)):
        if string[i] == reference[i]:
            result.append('right')
        elif string[i] in reference:
            result.append('position')
        else:
            result.append('wrong')
    return result