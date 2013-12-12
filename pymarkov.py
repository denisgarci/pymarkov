import sys
import pickle
import os.path
from collections import defaultdict
from random import choice, randrange
from itertools import izip, islice
from collections import Counter

from nltk.tokenize import sent_tokenize, word_tokenize


def pickled(func):

    def wrapper(other, file_name):
        root, ext = os.path.splitext(file_name)
        pickled_file_name = root + '-pickled' + ext
        try:
            with open(pickled_file_name) as f:
                result = pickle.load(f)
        except IOError:
            #so create file
            result = func(other, file_name)
            with open(pickled_file_name, 'w') as f:
                pickle.dump(result, f)
        return result

    return wrapper


class MarkovChainGenerator(object):
    def __init__(self, file_name, k=2):
        self.gram_length = k
        self.gram_dict = self.populate_dict(file_name)

    @pickled
    def populate_dict(self, file_name):
        """ (file_name) -> None
        Creates and populates gram_dict
        """
        gram_dict = defaultdict(Counter)
        with open(file_name) as word_file:
            text = word_file.read()
            for sent in sent_tokenize(text):
                if sent.isupper():
                    continue
                words = [None] + word_tokenize(sent) + [None]
                zipped = izip(*[words[i:]
                                for i in range(self.gram_length + 1)])
                for word_tuple in zipped:
                    gram = word_tuple[:self.gram_length]
                    word = word_tuple[self.gram_length]
                    gram_dict[gram][word] += 1

        return gram_dict

    def generate_sentence(self):
        """ () -> [string]
        Generates a sttring using the Markov chain...
        """
        start_keys = [k for k in self.gram_dict.keys() if k[0] is None]
        first_gram = choice(start_keys)
        sentence = list(first_gram[1:])
        current_gram = first_gram
        while True:
            next_word = self.random_word(self.gram_dict[current_gram])
            if next_word is None:
                return ' '.join(sentence)
            sentence.append(next_word)
            current_gram = tuple(sentence[-self.gram_length:])

    def random_word(self, freq_counter):
        """ (Counter) -> string
        Returns a random word based on the distribution given in the dict
        """
        random_index = randrange(sum(freq_counter.values()))
        return next(islice(freq_counter.elements(), random_index, None))


if __name__ == '__main__':
    a = MarkovChainGenerator("emily-dick.txt", 2)
    #print(a.gram_dict)
    for _ in range(int(sys.argv[1])):
        print(a.generate_sentence())
