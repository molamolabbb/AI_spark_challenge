import shutil
import os

import json
import yaml
import numpy as np
from glob import glob


def copy_images(mode):
    dir_path = f"/Users/kimjua/project/animal/{mode}/"
    images = glob(dir_path+'*/*.jpg')

    # copy images
    new_image_path  = dir_path+'images/'
    os.makedirs(new_image_path, exist_ok=True)

    for image in images:
        shutil.copy(image, new_image_path+image.split('/')[-1])

def bbox_to_center_scale(bbox, img_width, img_height):
    x1, y1, x2, y2 = bbox

    x = (x1+x2)/2/img_width
    y = (y1+y2)/2/img_height
    
    bbox_width = (x2-x1)/img_width
    bbox_height = (y2-y1)/img_height
    
    return x, y, bbox_width, bbox_height

def make_labelling_file(mode):
    # make yolo format labelling file (.txt)
    # ground truth, x_middle, y_middle, bbox_width, bbox_height
    
    dir_path = f"/Users/kimjua/project/animal/{mode}/"
    new_label_path = dir_path+'labels/'
    os.makedirs(new_label_path)
    jsons = glob(dir_path+'*/*.json')
    classes = {'pig':0, 'cow':1}

    for file in jsons:
        with open(file, 'r') as f:
            new_txt = file.split('/')[-1].replace('json', 'txt')
            label = json.load(f)
            img_width = label['label_info']['image']['width']
            img_height = label['label_info']['image']['height']
            new_file = open(new_label_path+new_txt, 'w+')    
            c = new_txt.split('_')[1]
            for i in label['label_info']['annotations']:
                bbox = i['bbox']
                bbox_info = bbox_to_center_scale(bbox, img_width, img_height)
                for_txt = ' '.join(map(str, bbox_info))
                for_txt = ' '.join((str(classes[c]), for_txt, '\n'))
                new_file.write(for_txt)
            new_file.close()        

def make_info_file():
    # make info/train.txt file
    # list of train/test image path
    dir_path = f'/Users/kimjua/project/animal/'
    os.makedirs(dir_path+'info', exist_ok=True)

    for mode in ['Training', 'Test']:
        images = glob(dir_path+f'{mode}/images/*jpg')
        if mode == 'Training':
            filename = dir_path+'info/train.txt'
        else:
            filename = dir_path+'info/test.txt'
        with open(filename, 'w+') as f:
            for img in images:
                f.write(img+'\n')
        f.close()

def make_yaml_file():
    # make data.yml file
    path = '/Users/kimjua/project/animal/data/'
    os.makedirs(path, exist_ok=True)
    object_list = ['pig', 'cow']
    with open(path+'data.yaml', 'w') as f:
        yaml.dump({
            'train':'../Train/info/train.txt',
            'test':'../Test/info/test.txt',
            'names': object_list, 'nc': len(object_list)}, f)
        f.close()

if __name__=='__main__':  
    copy_images('Training')
    copy_images('Test')

    make_labelling_file('Training')
    make_labelling_file('Test')

    make_info_file()        
    make_yaml_file()