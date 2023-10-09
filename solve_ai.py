from words import words
from process import *
import string
import numpy as np
import matplotlib.pyplot as plt

ALPHABET = string.ascii_uppercase
CHANCES = 6
CHARACTERS = 5

class App():
    
    def __init__(self, database):
        self.treated_words = list(map(lambda word: normalize_word(word), database))
        self.ocourrences = {}
        self.reset_current_dataset()
        while(True):
            for i in range(CHANCES):
                self.best_word=self.find_best_word_searching(debug=True)
                self.filter_dataset(input('Digite a palavra escrita:') or self.best_word ,input('Digite o relatorio da palavra (ex PPWWR):'))
            if input('Deseja jogar novamente? (s/n)') == 's':
                self.reset_current_dataset()
            else:
                break
            


        

    def count_word_ocourrences(self, database):
        for letter in ALPHABET:
            self.ocourrences[letter] = self.count_letters(letter, database)

    def count_letters(self, letter, database):
        return list(map(lambda word: letter in word, database)).count(True)

    def sort_by_value(self, data):
        return sorted(data, key= lambda pair: pair[1], reverse=True) 


    def graph_letter_distribution(self):
        letters = list(self.ocourrences.keys())
        values = list(self.ocourrences.values())

        fig = plt.figure(figsize = (10, 5))
        
        plt.bar(letters, values, color ='maroon',
                width = 0.4)
        
        plt.ylabel("Number of ocurrences")
        plt.title("Letter distribution")
        plt.show()

    def find_best_word_mantaining(self, debug=False):
        self.count_word_ocourrences(self.current_dataset)
        self.word_weights = {}

        for word in self.current_dataset:
            letters = list(dict.fromkeys(list(word)))
            self.word_weights[word] = 0 
            for letter in letters:
                self.word_weights[word] += self.ocourrences[letter]
            
        words = list(self.word_weights.keys())
        weights = list(self.word_weights.values())
        zipped = zip(words, weights)
        weights_sorted = self.sort_by_value(zipped)

        if debug:
            print('\nLista das palavras mais indicadas:')
            for i in range(min(10, len(weights_sorted))):
                print(f'{i+1}º: {weights_sorted[i][0]} - {weights_sorted[i][1]}')
            print('')
        return weights_sorted[0][0]
    
    def find_best_word_searching(self, debug=False):        
        def filter_function(word, letter):
            if letter in word:
                if letter in self.discoveries['wrong']:
                    return False
                if letter in self.discoveries['right'].keys():
                    critical_positions = self.discoveries['right'][letter]
                    for critical_position in critical_positions:
                        if word[critical_position] == letter:
                            return word.count(letter) > len(critical_positions)
                    return True

                elif letter in self.discoveries['position'].keys():
                    critical_positions = self.discoveries['position'][letter]
                    for critical_position in critical_positions:
                        if word[critical_position] == letter:
                            return word.count(letter) > len(critical_positions)
                    return True
                else:
                    return True
            else:
                return False
            
        for letter in ALPHABET:
            self.ocourrences[letter] = list(map(lambda word, letter=letter:filter_function(word, letter), self.current_dataset)).count(True)
        self.word_weights = {}

        for word in self.treated_words:
            letters = list(dict.fromkeys(list(word)))
            self.word_weights[word] = 0 
            for i in range(len(letters)):
                letter = letters[i]

                if letter in self.discoveries['wrong']:
                    self.word_weights[word] = 0
                    break
                if letter in self.discoveries['position'].keys():
                    # if not i in self.discoveries['position'][letter]:
                    #     self.word_weights[word] += self.ocourrences[letter]
                    if i in self.discoveries['position'][letter]:
                        self.word_weights[word] = 0
                        break
                if letter in self.discoveries['right'].keys():
                    if not i in self.discoveries['right'][letter]:
                        self.word_weights[word] += self.ocourrences[letter]
                    # if i in self.discoveries['right'][letter]:
                    #     self.word_weights[word] = 0
                
                else:
                    self.word_weights[word] += self.ocourrences[letter]
            
        words = list(self.word_weights.keys())
        weights = list(self.word_weights.values())
        zipped = zip(words, weights)
        weights_sorted = self.sort_by_value(zipped)

        if debug:
            print('\nLista das palavras mais indicadas:')
            for i in range(min(10, len(weights_sorted))):
                print(f'{i+1}º: {weights_sorted[i][0]} - {weights_sorted[i][1]}')
            print('')
        return weights_sorted[0][0]

    
    def reset_current_dataset(self):
        self.current_dataset = self.treated_words.copy()
        self.discoveries = {
            'right': {},
            'position': {},
            'wrong': []
        }

    def filter_dataset(self, word, results):
        for i in range(len(word)):
            letter = word[i]
            info = results[i]
            match info:
                case 'W':
                    self.current_dataset = list(filter(lambda word: letter not in word, self.current_dataset))
                    self.discoveries['wrong'].append(letter)
                case 'P':
                    self.current_dataset = list(filter(lambda word: letter in word and letter!=word[i], self.current_dataset))
                    if not hasattr(self.discoveries['position'], letter):
                        self.discoveries['position'][letter] = []
                    self.discoveries['position'][letter].append(i)
                case 'R':
                    self.current_dataset = list(filter(lambda word: letter in word and letter==word[i], self.current_dataset))
                    if not hasattr(self.discoveries['right'], letter):
                        self.discoveries['right'][letter] = []
                    self.discoveries['right'][letter].append(i)
                case '_':
                    pass
        

    

if __name__ == "__main__":
    App(words)
