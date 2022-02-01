#!/bin/bash
for i in $(seq 367 1 500)
do
	echo "$i"
	python3 AI_spark_challenge/make_submit_file.py --exp exp$i 
done

