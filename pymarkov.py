from collections import defaultdict
from random import choice, randrange
from itertools import izip

from nltk.tokenize import sent_tokenize, word_tokenize

class MarkovChainGenerator(object):

    def __init__(self, file_name, k=2):
        self.gram_length = k
        self.gram_dict = defaultdict(lambda : defaultdict(int))
        self.populate_dict(file_name)

    def populate_dict(self, file_name):
        with open(file_name) as word_file:
            text = word_file.read()
            for sent in sent_tokenize(text):
                words = [None] + word_tokenize(sent) + [None]
                for gram in izip(*[words[i:] for i in range(self.gram_length + 1)]):
                    key = gram[:self.gram_length]
                    value = gram[self.gram_length]
                    self.gram_dict[key][value] += 1

    def generate_sentence(self):
        """ (self) -> [string]
        Generates a sttring using the Markov chain...
        """
        start_keys = [k for k in self.gram_dict.keys() if k[0] is None]
        first_gram = choice(start_keys)
        sentence = list(first_gram[1:])
        current_gram = first_gram
        while True:
            next_word = self.random_word(self.gram_dict[current_gram])
            if next_word is None:
                return sentence
            sentence.append(next_word)
            current_gram = tuple(sentence[-self.gram_length:])

    def random_word(self, freq_dict):
        """ (self, dict) -> string
        Returns a random word based on the distribution given in the dict
        """
        total = sum(freq_dict.values())
        random_index = randrange(total)
        freq_sum  = 0
        for k, v in freq_dict.iteritems():
            freq_sum += v
            if random_index < freq_sum:
                return k




if __name__ == '__main__':
    a = MarkovChainGenerator("moby-dick.txt", 2)
    #print(a.gram_dict)
    print(' '.join(a.generate_sentence()))

