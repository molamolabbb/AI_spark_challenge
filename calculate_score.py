from sys import argv
import pandas as pd
from map_boxes import mean_average_precision_for_boxes


def calcuate_map(ans_path='answer.csv', pred_path='submit.csv'):
    ans = pd.read_csv(ans_path)
    pred = pd.read_csv(pred_path)

    pred = pred[['ImageID', 'LabelName', 'Conf', 'XMin', 'XMax', 'YMin', 'YMax']]

    # pred = pred.sort_values(by=['Conf'], ignore_index=True)
    ans = ans.sort_values(by=['ImageID'], ignore_index=True)
    pred = pred.sort_values(by=['ImageID'], ignore_index=True)

    ans_images = list(ans['ImageID'].unique())

    for image_name in ans_images:
        width, height = ans[ans['ImageID'] == image_name][['Width', 'Height']].values[0]
        pred.loc[pred['ImageID'] == image_name, 'XMin':'XMax'] /= width
        pred.loc[pred['ImageID'] == image_name, 'YMin':'YMax'] /= height

    ans_arr = ans[['ImageID', 'LabelName', 'XMin', 'XMax', 'YMin', 'YMax']].values
    pred_arr = pred[['ImageID', 'LabelName', 'Conf', 'XMin', 'XMax', 'YMin', 'YMax']].values

    mean_ap, ap = mean_average_precision_for_boxes(ans_arr, pred_arr, iou_threshold=0.75, verbose=False)

    mean_ap = round(mean_ap, 5)

    print(f'score:{mean_ap}')