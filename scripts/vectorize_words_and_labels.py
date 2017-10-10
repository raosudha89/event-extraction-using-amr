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

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: python vectorize_words_and_labels.py <train_dest_dir> <test_dest_dir> <list_of_words.p>"
		sys.exit(0)
	train_dest_dir = sys.argv[1]
	test_dest_dir = sys.argv[2]
	path_words_list_train = []
	path_label_list_train = []
	path_words_list_test = []
	path_label_list_test = []
	for i in range(3, len(sys.argv)):
		if "train" in sys.argv[i]:
			path_words_list_train += get_words_without_edges(p.load(open(sys.argv[i], 'rb')))
			path_label_list_train += p.load(open(sys.argv[i][:-8]+"_labels.p", 'rb'))
		else:
			path_words_list_test += get_words_without_edges(p.load(open(sys.argv[i], 'rb')))
			path_label_list_test += p.load(open(sys.argv[i][:-8]+"_labels.p", 'rb'))
	all_path_words_list = path_words_list_train + path_words_list_test
	vocab = sorted(reduce(lambda x, y: x | y, (set(path_words) for path_words in all_path_words_list)))
	vocab_size = len(vocab) + 1
	vocab_dim = 100
	word_embeddings = np.zeros((vocab_size, vocab_dim))
	for index, word in enumerate(vocab):
		word_embeddings[index] = get_wordvector(word)
	p.dump(path_words_list_train, open(os.path.join(train_dest_dir, "path_words_list.p"), 'wb'))
	p.dump(path_label_list_train, open(os.path.join(train_dest_dir, "path_label_list.p"), 'wb'))
	p.dump(path_words_list_test, open(os.path.join(test_dest_dir, "path_words_list.p"), 'wb'))
	p.dump(path_label_list_test, open(os.path.join(test_dest_dir, "path_label_list.p"), 'wb'))
	p.dump(word_embeddings, open(os.path.join(train_dest_dir, "word_embeddings.p"), 'wb'))
	p.dump(vocab, open(os.path.join(train_dest_dir, "vocab.p"), 'wb'))	
