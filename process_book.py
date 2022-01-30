import nltk
from nltk.tokenize import sent_tokenize

def split_sentence(filename):
    with open(filename) as f:
        lines = ''.join([line.strip().strip('*') for line in f])
        f.close()
        return sent_tokenize(lines)

