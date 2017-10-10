#!/bin/sh
dirname=$1
mkdir $dirname"_preprocessed"
for f in $dirname/PMC-33*.a1
do
	s=$(basename "$f")
	filename=${s%.a1}
	bioamrparser/run.sh -a $dirname"_preprocessed/"$filename.txt.replaced.lines $dirname"_preprocessed/"$filename.txt.replaced.lines.untok.amr
done
