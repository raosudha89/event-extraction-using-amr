#!/bin/bash
#PBS -l walltime=48:00:00
cd /fs/clip-amr/isi-internship
source /fs/clip-amr/isi-internship/theano-env/bin/activate
python scripts/vectorize_words_and_labels.py data/BioNLP09_11_13/train/ data/BioNLP09_11_13/devel data/BioNLP09_11_13/train/*_words.p data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_preprocessed/*_words.p 
