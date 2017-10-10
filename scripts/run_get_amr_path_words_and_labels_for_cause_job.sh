#!/bin/bash
#PBS -l walltime=4:00:00
#PBS -l nodes=1
#PBS -l mem=1gb
#PBS -l pmem=1gb
cd /fs/clip-amr/isi-internship
source /fs/clip-amr/isi-internship/theano-env/bin/activate
#sh scripts/run_get_amr_path_words_and_labels_for_cause.sh data/BioNLP09/bionlp09_shared_task_training_data_rev2
#sh scripts/run_get_amr_path_words_and_labels_for_cause.sh data/BioNLP09/bionlp09_shared_task_development_data_rev1 
#sh scripts/run_get_amr_path_words_and_labels_for_cause.sh data/BioNLP11/BioNLP-ST_2011_genia_train_data_rev1
#sh scripts/run_get_amr_path_words_and_labels_for_cause.sh data/BioNLP13/BioNLP-ST-2013_GE_train_data_rev3
sh scripts/run_get_amr_path_words_and_labels_for_cause.sh data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3
