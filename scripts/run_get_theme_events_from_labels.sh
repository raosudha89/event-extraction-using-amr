#!/bin/sh
dirname=$1
for f in $dirname/*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	#python scripts/get_theme_events_from_labels_v4.py $dirname"_preprocessed/"$filename"_labels.p" $dirname"_preprocessed/"$filename"_event_info.p" $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_output/"$filename".a2"  
	python scripts/get_theme_events_from_labels_v4.py $dirname"_preprocessed/"$filename"_labels_predicted.p" $dirname"_preprocessed/"$filename"_event_info.p" $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_output/"$filename".a2" 
done
