#!/bin/sh
dirname=$1
for f in $dirname/*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	python scripts/get_amr_path_words_and_labels_for_theme.py $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_preprocessed/"$filename.txt.replaced $dirname/$filename.a1 $dirname/$filename.a2
done
