import os
import json
import shutil
import random
import numpy as np
from tqdm import tqdm

Dataset_root = '/mnt/e/whyu/zxh_salmo/Speed/speed_new'
os.chdir(os.path.join(Dataset_root, 'images'))

classes = {
    'fish':0
}

test_frac = 0.2  # 测试集比例
random.seed(123) # 随机数种子，便于复现

# ========================================================================================

# 工具函数
def process_single_json(labelme_path, save_folder='../../labels/train'):
    
    # 载入 labelme格式的 json 标注文件
    with open(labelme_path, 'r', encoding='utf-8') as f:
        labelme = json.load(f)
        
    img_width = labelme['imageWidth']   # 图像宽度
    img_height = labelme['imageHeight'] # 图像高度
    
    # 生成 YOLO 格式的 txt 文件
    suffix = labelme_path.split('.')[-2]
    yolo_txt_path = suffix + '.txt'
    
    with open(yolo_txt_path, 'w', encoding='utf-8') as f:
        for each_ann in labelme['shapes']: # 遍历每个框

            if each_ann['shape_type'] == 'rectangle': # 筛选出框

                # 获取类别 ID
                bbox_class_id = classes[each_ann['label']]

                # 左上角和右下角的 XY 像素坐标
                bbox_top_left_x = int(min(each_ann['points'][0][0], each_ann['points'][1][0]))
                bbox_bottom_right_x = int(max(each_ann['points'][0][0], each_ann['points'][1][0]))
                bbox_top_left_y = int(min(each_ann['points'][0][1], each_ann['points'][1][1]))
                bbox_bottom_right_y = int(max(each_ann['points'][0][1], each_ann['points'][1][1]))

                # 框中心点的 XY 像素坐标
                bbox_center_x = int((bbox_top_left_x + bbox_bottom_right_x) / 2)
                bbox_center_y = int((bbox_top_left_y + bbox_bottom_right_y) / 2)

                # 框宽度
                bbox_width = bbox_bottom_right_x - bbox_top_left_x

                # 框高度
                bbox_height = bbox_bottom_right_y - bbox_top_left_y

                # 框中心点归一化坐标
                bbox_center_x_norm = bbox_center_x / img_width
                bbox_center_y_norm = bbox_center_y / img_height

                # 框归一化宽度
                bbox_width_norm = bbox_width / img_width
                # 框归一化高度
                bbox_height_norm = bbox_height / img_height

                # 生成 YOLO 格式的一行标注，指定保留小数点后几位
                bbox_yolo_str = '{} {:.4f} {:.4f} {:.4f} {:.4f}'.format(bbox_class_id, bbox_center_x_norm, bbox_center_y_norm, bbox_width_norm, bbox_height_norm)
                # 写入 txt 文件中
                f.write(bbox_yolo_str + '\n')

    shutil.move(yolo_txt_path, save_folder)
    print('{} --> {} 转换完成'.format(labelme_path, yolo_txt_path))


folder = '.'

img_paths = os.listdir(folder)
random.shuffle(img_paths) # 随机打乱

val_number = int(len(img_paths) * test_frac) # 测试集文件个数
train_files = img_paths[val_number:]         # 训练集文件名列表
val_files = img_paths[:val_number]           # 测试集文件名列表

os.mkdir('train')
for each in tqdm(train_files):
    shutil.move(each, 'train')

os.mkdir('val')
for each in tqdm(val_files):
    shutil.move(each, 'val')

os.chdir('../labelme_jsons')
os.mkdir('train')
for each in tqdm(train_files):
    srt_path = each.split('.')[0] + '.json'
    shutil.move(srt_path, 'train')

os.mkdir('val')
for each in tqdm(val_files):
    srt_path = each.split('.')[0] + '.json'
    shutil.move(srt_path, 'val')

os.chdir('../')

os.mkdir('labels')
os.mkdir('labels/train')
os.mkdir('labels/val')

os.chdir('labelme_jsons/train')

save_folder = '../../labels/train'
for labelme_path in os.listdir():
    process_single_json(labelme_path, save_folder=save_folder)
print('YOLO格式的txt标注文件已保存至 ', save_folder)

os.chdir('../../')

os.chdir('labelme_jsons/val')

save_folder = '../../labels/val'
for labelme_path in os.listdir():
    process_single_json(labelme_path, save_folder=save_folder)
print('YOLO格式的txt标注文件已保存至 ', save_folder)








