import os
import json
import shutil
import random
import numpy as np
from tqdm import tqdm

Dataset_root = '/mnt/e/whyu/zxh_salmo/Speed/speed_new'
os.chdir(os.path.join(Dataset_root, 'labelme_jsons'))

class_list= [
    {'id': 0, 'name': 'fish'}
]

test_frac = 0.2  # 测试集比例
random.seed(123) # 随机数种子，便于复现

# ========================================================================================

# 工具函数
def process_single_json(labelme, image_id=1):
    '''
    输入labelme的json数据，输出coco格式的每个框的关键点标注信息
    '''
    
    global ANN_ID
    
    coco_annotations = []
    
    for each_ann in labelme['shapes']: # 遍历该json文件中的所有标注

        if each_ann['shape_type'] == 'rectangle': # 筛选出框

            ## 该框的元数据
            bbox_dict = {}
            # 该框的类别 信息
            bbox_dict['category_id'] = label2id[each_ann['label']]
            bbox_dict['segmentation'] = []
            
            bbox_dict['iscrowd'] = 0
            bbox_dict['image_id'] = image_id
            bbox_dict['id'] = ANN_ID
            ANN_ID += 1

            # 获取框坐标
            bbox_left_top_x = min(int(each_ann['points'][0][0]), int(each_ann['points'][1][0]))
            bbox_left_top_y = min(int(each_ann['points'][0][1]), int(each_ann['points'][1][1]))
            bbox_right_bottom_x = max(int(each_ann['points'][0][0]), int(each_ann['points'][1][0]))
            bbox_right_bottom_y = max(int(each_ann['points'][0][1]), int(each_ann['points'][1][1]))
            bbox_w = bbox_right_bottom_x - bbox_left_top_x
            bbox_h = bbox_right_bottom_y - bbox_left_top_y
            bbox_dict['bbox'] = [bbox_left_top_x, bbox_left_top_y, bbox_w, bbox_h] # 左上角x、y、框的w、h
            bbox_dict['area'] = bbox_w * bbox_h
            
            # 筛选出分割多段线
            for each_ann in labelme['shapes']: # 遍历所有标注
                if each_ann['shape_type'] == 'polygon': # 筛选出分割多段线标注
                    # 第一个点的坐标
                    first_x = each_ann['points'][0][0]
                    first_y = each_ann['points'][0][1]
                    if (first_x>bbox_left_top_x) & (first_x<bbox_right_bottom_x) & (first_y<bbox_right_bottom_y) & (first_y>bbox_left_top_y): # 筛选出在该个体框中的关键点
                        bbox_dict['segmentation'] = list(map(lambda x: list(map(lambda y: round(y, 2), x)), each_ann['points'])) # 坐标保留两位小数
                    
            coco_annotations.append(bbox_dict)
            
    return coco_annotations

def process_folder():
    IMG_ID = 0
    ANN_ID = 0

    # 遍历所有 labelme 格式的 json 文件
    for labelme_json in os.listdir(): 

        if labelme_json.split('.')[-1] == 'json':

            with open(labelme_json, 'r', encoding='utf-8') as f:

                labelme = json.load(f)

                ## 提取图像元数据
                img_dict = {}
                img_dict['file_name'] = labelme['imagePath']
                img_dict['height'] = labelme['imageHeight']
                img_dict['width'] = labelme['imageWidth']
                img_dict['id'] = IMG_ID
                coco['images'].append(img_dict)

                ## 提取框和关键点信息
                coco_annotations = process_single_json(labelme, image_id=IMG_ID)
                coco['annotations'] += coco_annotations

                IMG_ID += 1

                print(labelme_json, '已处理完毕')

        else:
            pass


folder = '.'

img_paths = os.listdir(folder)
random.shuffle(img_paths) # 随机打乱

val_number = int(len(img_paths) * test_frac) # 测试集文件个数
train_files = img_paths[val_number:]         # 训练集文件名列表
val_files = img_paths[:val_number]           # 测试集文件名列表

# 创建文件夹，存放训练集的 labelme格式的 json 标注文件
train_labelme_jsons_folder = 'train_labelme_jsons'
os.mkdir(train_labelme_jsons_folder)

for each in tqdm(train_files):
    src_path = os.path.join(folder, each)
    dst_path = os.path.join(train_labelme_jsons_folder, each)
    shutil.move(src_path, dst_path)

# 创建文件夹，存放训练集的 labelme格式的 json 标注文件
val_labelme_jsons_folder = 'val_labelme_jsons'
os.mkdir(val_labelme_jsons_folder)

for each in tqdm(val_files):
    src_path = os.path.join(folder, each)
    dst_path = os.path.join(val_labelme_jsons_folder, each)
    shutil.move(src_path, dst_path)

label2id = {}
for each in class_list:
    label2id[each['name']] = each['id']

# 转换训练集的所有labelme标注文件
coco = {}

coco['categories'] = class_list

coco['images'] = []
coco['annotations'] = []

IMG_ID = 0
ANN_ID = 0

path = os.path.join(Dataset_root, 'labelme_jsons', 'train_labelme_jsons')
os.chdir(path)

process_folder()

# 保存coco标注文件
coco_path = '../../train_coco.json'
with open(coco_path, 'w') as f:
    json.dump(coco, f, indent=2)

os.chdir('../../')

# 转换测试集的所有labelme标注文件
coco = {}

coco['categories'] = class_list

coco['images'] = []
coco['annotations'] = []

IMG_ID = 0
ANN_ID = 0

path = os.path.join('labelme_jsons', 'val_labelme_jsons')
os.chdir(path)

process_folder()

# 保存coco标注文件
coco_path = '../../val_coco.json'
with open(coco_path, 'w') as f:
    json.dump(coco, f, indent=2)

os.chdir('../../')