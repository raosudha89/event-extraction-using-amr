#perl data/BioNLP11/BioNLP-ST_2011_genia_tools_rev1/a2-decompose.pl data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_output/*.a2
#perl data/BioNLP11/BioNLP-ST_2011_genia_tools_rev1/a2d-evaluate.pl -g data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3 -S data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_output/*.a2d
#perl data/BioNLP11/BioNLP-ST_2011_genia_tools_rev1/a2-evaluate.pl -g data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3 -t1 data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_output/*.a2
perl data/BioNLP11/BioNLP-ST_2011_genia_tools_rev1/a2-evaluate.pl -g data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3 -t2 -sp data/BioNLP13/BioNLP-ST-2013_GE_devel_data_rev3_output/*.a2
