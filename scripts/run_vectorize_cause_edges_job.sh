#!/bin/bash
#PBS -l walltime=4:00:00
#PBS -l nodes=1
#PBS -l mem=1gb
#PBS -l pmem=1gb
cd /fs/clip-amr/isi-internship
source /fs/clip-amr/isi-internship/theano-env/bin/activate
python scripts/vectorize_edges.py data/BioNLP09_11_13/train/cause data/BioNLP09_11_13/devel/cause data/BioNLP09_11_13/train/cause/*_words.p data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_preprocessed/cause/*_words.p
