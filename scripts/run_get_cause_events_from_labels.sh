#!/bin/sh
dirname=$1
for f in $dirname/*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	python scripts/get_cause_events_from_labels.py $dirname"_preprocessed/"$filename"_output_interactions.p" $dirname"_preprocessed/"$filename"_output_theme_events.p" $dirname"_preprocessed/cause/"$filename"_labels.p" $dirname"_preprocessed/cause/"$filename"_event_info.p" $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_output/"$filename".a2"  
	#python scripts/get_cause_events_from_labels.py $dirname"_preprocessed/"$filename"_output_interactions.p" $dirname"_preprocessed/"$filename"_output_theme_events.p" $dirname"_preprocessed/cause/"$filename"_labels_predicted.p" $dirname"_preprocessed/cause/"$filename"_event_info.p" $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs.p $dirname"_output/"$filename".a2"  
done
