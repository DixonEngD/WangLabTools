import torch
import torchvision
from torchvision import transforms
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np

# 定义数据增强的转换
transform = transforms.Compose([
    transforms.RandomResizedCrop(640), # 随机裁剪并调整大小为640x640
    transforms.RandomHorizontalFlip(), # 随机水平翻转
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(45), # 随机旋转
    transforms.ColorJitter(brightness=0.5, contrast=0.2, saturation=0.2, hue=0.1), # 随机颜色调整
    transforms.ToTensor(), # 转换为张量
])

input_folder = r'E:\yolov5\dxb\original\3'

output_folder = r'E:\yolov5\dxb\enhancement\3'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_list = os.listdir(input_folder)

count = 1

for file in file_list:
    image_path = os.path.join(input_folder, file)
    image = Image.open(image_path)
    for i in range(10): # 假设生成10张增强后的图片
        augmented_image = transform(image)
        save_path = os.path.join(output_folder, '{:05d}.jpg'.format(count))
        count += 1
        torchvision.utils.save_image(augmented_image, save_path)

print("增强后的图片已保存到", output_folder)