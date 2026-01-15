from PIL import Image
import os

# 定义输入文件夹和输出文件夹
input_folder = r'E:\data\sy\3d\wh_mx'  # 替换为你的图片文件夹路径
output_folder = r'E:\data\sy\3d\wh_mx_split'  # 替换为保存分割图片的文件夹路径

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 支持的图片格式
supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')

# 获取输入文件夹中的所有图片文件
image_files = [f for f in os.listdir(input_folder) 
              if f.lower().endswith(supported_formats)]

# 按文件名排序，确保顺序正确
image_files.sort()

print(f"Found {len(image_files)} images to process.")

# 分割图片并保存
for i, file_name in enumerate(image_files):
    # 构造完整路径
    file_path = os.path.join(input_folder, file_name)
    
    try:
        # 打开图片
        img = Image.open(file_path)
        
        # 确保图片是4416x1242
        if img.size != (4416, 1242):
            print(f"Skipping {file_name}, size {img.size} is not 4416x1242.")
            continue
        
        # 分割图片
        left_img = img.crop((0, 0, 2208, 1242))
        right_img = img.crop((2208, 0, 4416, 1242))
        
        # 生成保存路径（使用原文件名前缀）
        name_without_ext = os.path.splitext(file_name)[0]
        left_img_path = os.path.join(output_folder, f'left_{name_without_ext}.png')
        right_img_path = os.path.join(output_folder, f'right_{name_without_ext}.png')
        
        # 保存图片
        left_img.save(left_img_path)
        right_img.save(right_img_path)
        
        print(f"Processed {file_name} -> {os.path.basename(left_img_path)}, {os.path.basename(right_img_path)}")
        
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

print(f"Done! Processed {len(image_files)} images.")