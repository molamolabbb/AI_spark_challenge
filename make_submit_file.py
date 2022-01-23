import os
import json
import csv
from glob import glob 
from calculate_score import calcuate_map

def get_bbox_format(x, y, box_w, box_h, img_w, img_h):
    x, y, box_w, box_h, img_w, img_h = map(float, (x, y, box_w, box_h, img_w, img_h))
    x1 = x-box_w/2
    x1 = x1*img_w
    x2 = x+box_w/2
    x2 = x2*img_w
    
    y1 = y-box_h/2
    y1 = y1*img_h
    y2 = y+box_h/2
    y2 = y2*img_h    
    return x1, x2, y1, y2    

if __name__=='__main__':
    path = '/Users/kimjua/project/animal/result/labels/'
    result_list = glob(path+'*.txt')

    classes = {'0':'pig', '1':'cow'}
    data = []
    for file in result_list:
        if 'pig' in file: c = '0'
        else: c = '1'
        test_json_path = f'/Users/kimjua/project/animal/Test/label_{classes[c]}/'

        result_file =  open(file, 'r') 
        image_id = file.split('/')[-1].replace('txt','jpg')

        json_file = file.split('/')[-1].replace('txt','json')
        json_file = open(test_json_path+json_file)
        info = json.load(json_file)

        img_w = info['label_info']['image']['width']
        img_h = info['label_info']['image']['height']

        json_file.close()

        lines = result_file.readlines()
        for line in lines:
            animal, x, y, box_w, box_h, confidence = line.split()
            x_min, x_max, y_min, y_max  = get_bbox_format(x, y, box_w, box_h, img_w, img_h)
            data.append([image_id, classes[animal], confidence, x_min, x_max, y_min, y_max])
        result_file.close()

    header = ["ImageID", "LabelName", "Conf", "XMin", "XMax", "YMin", "YMax"]
    with open('submit.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)
        f.close()
        
    # calculate map score
    calcuate_map(ans_path='answer.csv', pred_path='submit.csv')