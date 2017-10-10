import sys, os
import pickle as p

if __name__ == "__main__":
	if True:
		if len(sys.argv) < 2:
			print "usage: python separate_predicted_labels.py <data_predicted_labels> <list_of_labels.p>"
			sys.exit(0)
		data_predicted_labels = p.load(open(sys.argv[1], 'rb'))
		label_start_index = 0
		for i in range(2, len(sys.argv)):
			#print sys.argv[i]
			true_labels = p.load(open(sys.argv[i], 'rb'))
			label_end_index = label_start_index+len(true_labels)
			assert(label_end_index <= len(data_predicted_labels))
			predicted_labels = data_predicted_labels[label_start_index:label_end_index]
			label_start_index = label_end_index
			p.dump(predicted_labels, open(sys.argv[i][:-9]+"_labels_predicted.p", 'wb'))
		if label_start_index != len(data_predicted_labels):
			print label_start_index, len(data_predicted_labels)
			print "Mismatch!!!"
