import albumentations as A
import numpy as np
import cv2
import os
from PIL import Image
from albumentations.pytorch import ToTensorV2

# 定义数据增强转换
def get_transforms():
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
        A.ColorJitter(p=0.3),
        A.RandomBrightnessContrast(p=0.3),
        A.RandomScale(scale_limit=0.2, p=0.5),
        A.Resize(height=640, width=640),
        ToTensorV2()  # 转换为 PyTorch 张量
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels']))

# 读取 YOLO 格式的标签文件
def read_labels(label_path):
    with open(label_path, 'r') as file:
        labels = [list(map(float, line.strip().split())) for line in file]
    return labels

# 保存 YOLO 格式的标签文件
def save_labels(labels, output_path):
    with open(output_path, 'w') as file:
        for label in labels:
            file.write(' '.join(map(str, label)) + '\n')

# 处理单张图像和标签，生成多个增强版本
def process_image_and_labels(image_path, label_path, output_dir, num_augmentations):
    # 读取图像
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为 RGB 格式

    # 读取标签
    labels = read_labels(label_path)
    
    for i in range(num_augmentations):
        # 数据增强
        transform = get_transforms()
        
        # 提取坐标和标签
        bboxes = [label[1:] for label in labels]  # 提取框的坐标
        labels_classes = [label[0] for label in labels]  # 提取类别
        
        # 增强操作
        augmented = transform(image=image, bboxes=bboxes, labels=labels_classes)
        
        augmented_image = augmented['image']
        augmented_labels = augmented['bboxes']
        
        # 保存增强后的图像
        augmented_image_pil = Image.fromarray(np.transpose(augmented_image.numpy(), (1, 2, 0)))  # 转换为 PIL 格式
        image_name = os.path.basename(image_path)
        augmented_image_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_aug_{i}.jpg")
        augmented_image_pil.save(augmented_image_path)
        
        # 保存增强后的标签
        augmented_labels_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_aug_{i}.txt")
        save_labels(augmented_labels, augmented_labels_path)

# 批量处理数据集
def process_dataset(image_dir, label_dir, output_dir, num_augmentations=5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for image_name in os.listdir(image_dir):
        if image_name.endswith('.jpg') or image_name.endswith('.png'):
            image_path = os.path.join(image_dir, image_name)
            label_path = os.path.join(label_dir, os.path.splitext(image_name)[0] + '.txt')
            
            if os.path.exists(label_path):
                process_image_and_labels(image_path, label_path, output_dir, num_augmentations)
            else:
                print(f"Label file for {image_name} does not exist.")

if __name__ == "__main__":
    image_dir = r'E:\dxb\original\111\images'
    label_dir = r'E:\dxb\original\111\labels'
    output_dir = r'E:\dxb\original\222'
    
    process_dataset(image_dir, label_dir, output_dir)
