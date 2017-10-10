import sys, os
import theano, lasagne, cPickle, time                                                   
import numpy as np
import theano.tensor as T     
from collections import OrderedDict, Counter
import pickle as p
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report

NO_OF_CLASSES = 2
WORD_EMBEDDING_DIM = 100
def iterate_minibatches(inputs, masks, labels, batch_size, shuffle=False):
    assert len(inputs) == len(labels)
    assert len(inputs) == len(masks)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batch_size]
        else:
            excerpt = slice(start_idx, start_idx + batch_size)
        yield inputs[excerpt], masks[excerpt], labels[excerpt]

def validate(name, val_fn, fold):
    corr = 0
    total = 0
    c = Counter()
    sents, masks, labels = fold
    preds = val_fn(sents, masks)
    preds = np.argmax(preds, axis=1)
    print classification_report(labels, preds)

    # for s, m, l in iterate_minibatches(sents, masks, labels, 100):
    for i, pred in enumerate(preds):
        if pred == labels[i]:
            corr += 1
        total += 1
        c[pred] += 1

    lstring = 'fold:%s, corr:%d, total:%d, acc:%f' %\
        (name, corr, total, float(corr) / float(total))
    print lstring
    print c
    return lstring

def build_lstm(len_voc, d_word, d_van,
    num_labels, max_len, We, freeze=False, temp=5., eps=1e-6, lr=0.1, rho=1e-5):
    
    # input theano vars
    sents = T.imatrix(name='sentence')
    masks = T.matrix(name='mask')
    labels = T.ivector('target')

    # define network
    l_in = lasagne.layers.InputLayer(shape=(None, max_len), input_var=sents)
    l_mask = lasagne.layers.InputLayer(shape=(None, max_len), input_var=masks)
    l_emb = lasagne.layers.EmbeddingLayer(l_in, len_voc, d_word, W=We)

    # now feed sequences of spans into VAN
    l_lstm = lasagne.layers.LSTMLayer(l_emb, d_van, mask_input=l_mask, )

    # freeze embeddings
    if freeze:
        l_emb.params[l_emb.W].remove('trainable')

    # now predict
    l_forward_slice = lasagne.layers.SliceLayer(l_lstm, -1, 1)
    l_out = lasagne.layers.DenseLayer(l_forward_slice, num_units=num_labels,\
        nonlinearity=lasagne.nonlinearities.softmax)

    # objective computation
    preds = lasagne.layers.get_output(l_out)
    loss = T.sum(lasagne.objectives.categorical_crossentropy(preds, labels))
    #loss = T.sum(lasagne.objectives.binary_crossentropy(preds, labels))
    loss += rho * sum(T.sum(l ** 2) for l in lasagne.layers.get_all_params(l_out))
    all_params = lasagne.layers.get_all_params(l_out, trainable=True)

    updates = lasagne.updates.adam(loss, all_params, learning_rate=lr)

    train_fn = theano.function([sents, masks, labels], [preds, loss], updates=updates)
    val_fn = theano.function([sents, masks], preds)
    debug_fn = theano.function([sents, masks], lasagne.layers.get_output(l_lstm))
    return train_fn, val_fn, debug_fn

def vectorize_path(path_words_list, path_label_list, word_idx, path_maxlen):
	X = []
	Y = []
	masks = []
	for i in range(len(path_words_list)):
		path_words = path_words_list[i]
		x = [word_idx[w] for w in path_words]
		mask = [1.0]*len(path_words)
		X.append(x)
		masks.append(mask)
		path_label = path_label_list[i]
		Y.append(path_label)
	return pad_sequences(X, maxlen=path_maxlen, padding='post'), pad_sequences(masks, maxlen=path_maxlen, padding='post'), np.asarray(Y, dtype='int32')	

def get_path_words_edges_list(path_words_list, path_edges_list):
	path_words_edges_list = []
	for i in range(len(path_words_list)):
		path_words = path_words_list[i]
		path_edges = path_edges_list[i]
		path_words_edges = []
		assert(len(path_words) == len(path_edges)+1)
		for j in range(len(path_words)-1):
			path_words_edges.append(path_words[j])
			path_words_edges.append(path_edges[j])
		path_words_edges.append(path_words[-1])
		path_words_edges_list.append(path_words_edges)
	return path_words_edges_list

def update_edge_list(edge_label_list, path_edges_list):
	for path_edges in path_edges_list:
		for edge in path_edges:
			if edge not in edge_label_list:
				edge_label_list.append(edge)
	return edge_label_list

if __name__ == '__main__':
    np.set_printoptions(linewidth=160)

    #train, dev, test = cPickle.load(open('root_sst.pkl', 'rb'))
    #vocab = cPickle.load(open('data/vocab.pkl', 'rb'))
    #We = cPickle.load(open('data/We.pkl', 'rb')).T.astype('float32')

    path_words_list_train = p.load(open(sys.argv[1], 'rb'))
    path_label_list_train = p.load(open(sys.argv[2], 'rb'))
    path_words_list_test = p.load(open(sys.argv[3], 'rb'))
    path_label_list_test = p.load(open(sys.argv[4], 'rb'))
    word_embeddings = p.load(open(sys.argv[5], 'rb'))
    vocab = p.load(open(sys.argv[6], 'rb'))
    path_edges_list_train = p.load(open(sys.argv[7], 'rb'))
    path_edges_list_test = p.load(open(sys.argv[8], 'rb'))
    edge_label_list = p.load(open(sys.argv[9], 'rb')) 
    ds_path_edges_list_train = p.load(open(sys.argv[10], 'rb'))
    path_edges_list_train += ds_path_edges_list_train

    edge_label_list = update_edge_list(edge_label_list, path_edges_list_train)
    edge_label_list = update_edge_list(edge_label_list, path_edges_list_test)

    path_words_edges_list_train = get_path_words_edges_list(path_words_list_train, path_edges_list_train)
    path_words_edges_list_test = get_path_words_edges_list(path_words_list_test, path_edges_list_test)

    vocab = vocab + edge_label_list
    word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
    path_maxlen = 30
    #path_maxlen = max(map(len, (x for x in path_words_list_train + path_words_list_test)))
    
	train = vectorize_path(path_words_list_train, path_label_list_train, word_idx, path_maxlen)
    dev = vectorize_path(path_words_list_test, path_label_list_test, word_idx, path_maxlen)
    
    #train = vectorize_path(path_words_edges_list_train, path_label_list_train, word_idx, path_maxlen)
    #dev = vectorize_path(path_words_edges_list_test, path_label_list_test, word_idx, path_maxlen)

    vocab_size = len(vocab) + 1
    embedding_weights = np.zeros((vocab_size,WORD_EMBEDDING_DIM)).astype('float32')
    for idx in range(len(word_embeddings)):
        embedding_weights[idx,:] = word_embeddings[idx] 
        if np.all(word_embeddings[idx]==0) or not np.all(np.isnan(word_embeddings[idx])==False):
            embedding_weights[idx,:] = np.random.rand(100)

    for i in range(len(edge_label_list)):
        idx = i+len(word_embeddings)
        emb = np.zeros(100)
        emb[i] = 1 #encode edges as one-hot vector
        embedding_weights[idx,:] = emb


    We = embedding_weights
	
    # possible to-do: "root" symbol at end?
    len_voc = len(vocab)+1
    num_labels = NO_OF_CLASSES
    d_word = 100
    d_van = 100
    lr = 0.001
    rho = 1e-5
    freeze = True
    batch_size = 15
    n_epochs = 10
    temp = 1.
    max_len = train[0].shape[1]

    print 'len_voc', len_voc, 'max_len', max_len

    log_file = 'logs/batchreg-%f_dvan-%d_tanh.txt' % (rho, d_van)
    log = open(log_file, 'w')

    print 'compiling graph...'
    train_fn, val_fn, debug_fn = build_lstm(len_voc, d_word, d_van, 
        num_labels, max_len, We, freeze=freeze, temp=temp, lr=lr, rho=rho)
    print 'done compiling'

    # train network
    for epoch in range(n_epochs):
        cost = 0.
        sents, masks, labels = train
        start = time.time()
        num_batches = 0.
        for s, m, l in iterate_minibatches(sents, masks, labels, batch_size, shuffle=True):
            preds, loss = train_fn(s, m, l)
            cost += loss
            num_batches += 1

        lstring = 'epoch:%d, cost:%f, time:%d' % \
            (epoch, cost / num_batches, time.time()-start)
        print lstring
        log.write(lstring + '\n')

        trperf = validate('train', val_fn, train)
        devperf = validate('dev', val_fn, dev)
        log.write(trperf + '\n')
        log.write(devperf + '\n')
        log.flush()
        print '\n'

    sents, masks, labels = dev
    preds = val_fn(sents, masks)
    preds = np.argmax(preds, axis=1)
    print classification_report(labels, preds)
    p.dump(preds, open(os.path.join(os.path.dirname(sys.argv[3]), "data_predicted_cause_labels_vectors_fix_we_edges_ds_v2.p"), 'wb'))
