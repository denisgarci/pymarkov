from collections import defaultdict
from collections import deque
from random import choice, randint

class MarkovChainGenerator(object):

    end_marks = {'.', '!', '?', '...'}

    def __init__(self, file_name, k=2):
        self.tuple_length = k
        self.tuple_dict = defaultdict(lambda : defaultdict(int))
        self.populate_dict(file_name)

    def words(self, file_obj):
        for line in file_obj:
            for word in line.split():
                yield word

    def populate_dict(self, file_name):
        with open(file_name) as word_file:
            wordgen = self.words(word_file)
            key_deque = deque()
            for word in wordgen:
                if len(key_deque) < self.tuple_length: # populating the deque
                    key_deque.append(word)
                    continue

                # here len(key_deque) == tuple_length
                # deal with the previous key, word
                key = tuple(key_deque)
                self.tuple_dict[key][word] += 1
                # prepare the deque for the next word
                key_deque.popleft()
                key_deque.append(word)

    def generate_sentence(self):
        first = choice(self.tuple_dict.keys())
        sentence = []
        while len(sentence) < 20:


    def choose_dist(self, freq_dict):
        total = sum(freq_dict.keys())
        random_index = randint(total)
        freq_sum  = 0
        for k, v in freq_dict.iteritems():
            freq_sum += v
            if freq_sum >= random_index:
                return k




if __name__ == '__main__':
    a = MarkovChainGenerator("moby-dick.txt", 2)
    print(a.tuple_dict[('was','a')])

