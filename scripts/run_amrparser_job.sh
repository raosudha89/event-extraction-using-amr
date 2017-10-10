#!/bin/bash
#PBS -l walltime=4:00:00
#PBS -l nodes=1
#PBS -l mem=4gb
#PBS -l pmem=4gb
cd /fs/clip-amr/isi-internship
#sh scripts/run_amrparser.sh data/BioNLP09/bionlp09_shared_task_development_data_rev1
#sh scripts/run_amrparser.sh data/BioNLP09/bionlp09_shared_task_training_data_rev2
#sh scripts/run_amrparser.sh data/BioNLP11/BioNLP-ST_2011_genia_devel_data_rev1
#sh scripts/run_amrparser.sh data/BioNLP11/BioNLP-ST_2011_genia_train_data_rev1
sh scripts/run_amrparser.sh data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_new
#sh scripts/run_amrparser.sh data/BioNLP13/BioNLP-ST-2013_GE_train_data_rev3
