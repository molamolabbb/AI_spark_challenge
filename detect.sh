#!/bin/bash
for i in $(seq 0.0001 0.0001 0.001)
do
	for j in $(seq 0.3 0.02 0.7)
	do
		echo "$i $j"
		python3 detect.py --weights runs/detect/test/best4.pt --data dataset/data/data.yaml --source dataset/test/images/ --save-txt --save-conf --imgsz 960 --conf-thres $i --iou-thres $j --nosave
	done
done
