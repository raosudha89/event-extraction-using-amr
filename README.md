#General steps to run
1. scripts/run_amrparser_job.sh
2. scripts/run_collect_interaction_terms_job.sh

3. scripts/run_get_amr_path_words_and_labels_for_theme_job.sh
4. scripts/run_vectorize_words_and_labels_theme_job.sh
5. scripts/run_vectorize_theme_edges_job.sh 
6. lasagne/lstm_with_edges_ds.py OR lasagne/lstm_with_edges.py
7. python scripts/separate_predicted_labels.py data/BioNLP09_11_13/devel/data_predicted_theme_labels.p data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_preprocessed/*_labels.p
8. scripts/run_get_theme_events_from_labels_job.sh


9. scripts/run_get_amr_path_words_and_labels_for_cause_job.sh
10. scripts/run_vectorize_words_and_labels_cause_job.sh  
11. scripts/run_vectorize_cause_edges_job.sh
12. lasagne/lstm_binary_for_cause_with_edges_ds.py OR lasagne/lstm_binary_for_cause_with_edges.py
13. python scripts/separate_predicted_labels.py data/BioNLP09_11_13/devel/cause/data_predicted_cause_labels.p data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_preprocessed/cause/*_labels.p   
14. scripts/run_get_cause_events_from_labels_job.sh 

15. scripts/run_evaluate.sh
