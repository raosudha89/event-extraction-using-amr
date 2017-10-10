#!/bin/sh
dirname=$1
for f in $dirname/*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	python scripts/get_amr_path_words_and_labels_for_cause.py $dirname/$filename.a1 $dirname"_preprocessed/"$filename.txt.replaced $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_preprocessed/"$filename"_output_theme_events.p" $dirname"_preprocessed/"$filename"_output_theme_events_info.p"
done
