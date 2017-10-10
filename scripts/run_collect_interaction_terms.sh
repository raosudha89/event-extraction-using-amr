#!/bin/sh
dirname=$1
python scripts/collect_interaction_terms.py $dirname 
for f in $dirname/*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	python scripts/amr_reader_with_alignments.py $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr > $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr_nx_graphs
done
