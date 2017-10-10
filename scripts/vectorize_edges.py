import sys, os
import numpy as np
import pickle as p

def get_only_edges(path_words_list):
	path_edges_list = []
	for words in path_words_list:
		edges = [words[k] for k in range(len(words)) if k % 2 != 0]
		path_edges_list.append(edges)
	return path_edges_list

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: python vectorize_edges.py <train_dest_dir> <test_dest_dir> <list_of_words.p>"
		sys.exit(0)
	train_dest_dir = sys.argv[1]
	test_dest_dir = sys.argv[2]
	path_edges_list_train = []
	path_edges_list_test = []
	for i in range(3, len(sys.argv)):
		if "train" in sys.argv[i]:
			path_edges_list_train += get_only_edges(p.load(open(sys.argv[i], 'rb')))
		else:
			path_edges_list_test += get_only_edges(p.load(open(sys.argv[i], 'rb')))
	p.dump(path_edges_list_train, open(os.path.join(train_dest_dir, "path_edges_list.p"), 'wb'))
	p.dump(path_edges_list_test, open(os.path.join(test_dest_dir, "path_edges_list.p"), 'wb'))
