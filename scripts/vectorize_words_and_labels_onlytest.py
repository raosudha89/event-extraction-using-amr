import sys, os
import numpy as np
import pickle as p
from wordvec import *

def get_words_without_edges(path_words_list):
	path_words_list_new = []
	for words in path_words_list:
		words = [words[k] for k in range(len(words)) if k % 2 == 0]
		path_words_list_new.append(words)
	return path_words_list_new

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: python vectorize_words_and_labels.py <test_dest_dir> <list_of_words.p>"
		sys.exit(0)
	train_word_embeddings = p.load(open(sys.argv[1], 'rb'))
	train_vocab = p.load(open(sys.arg[2], 'rb'))
	test_dest_dir = sys.argv[3]
	path_words_list_test = []
	path_label_list_test = []
	for i in range(4, len(sys.argv)):
		path_words_list_test += get_words_without_edges(p.load(open(sys.argv[i], 'rb')))
		path_label_list_test += p.load(open(sys.argv[i][:-8]+"_labels.p", 'rb'))
	test_vocab = sorted(reduce(lambda x, y: x | y, (set(path_words) for path_words in path_words_list_test)))
	vocab = merge_two_dicts(train_vocab, test_vocab)	
	test_vocab_size = len(test_vocab) + 1
	vocab_dim = 100
	test_word_embeddings = []
	for index, word in enumerate(test_vocab):
		if word not in train_vocab.values():
			test_word_embeddings[index] = get_wordvector(word)
	word_embeddings = np.concatenate((train_word_embeddings, test_word_embeddings))
	p.dump(path_words_list_test, open(os.path.join(test_dest_dir, "path_words_list.p"), 'wb'))
	p.dump(path_label_list_test, open(os.path.join(test_dest_dir, "path_label_list.p"), 'wb'))
	p.dump(word_embeddings, open(os.path.join(train_dest_dir, "word_embeddings.p"), 'wb'))
	p.dump(vocab, open(os.path.join(train_dest_dir, "vocab.p"), 'wb'))	

