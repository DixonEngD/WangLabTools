import os
import shutil

# 设置文件夹路径
source_folder = r'E:\whyu\zxh_salmo\breath\21'  # 源文件夹路径
target_folder = r'E:\whyu\zxh_salmo\breath\all\images'  # 目标文件夹路径

# 确保目标文件夹存在
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 获取源文件夹内所有文件
files = os.listdir(source_folder)

# 过滤出所有图片文件（根据文件扩展名进行过滤）
image_files = [f for f in files if f.lower().endswith('.png')]

# 对图片文件按字母顺序排序
image_files.sort()

# 重命名并复制到目标文件夹
start_num = 616  # 起始编号
for i, file_name in enumerate(image_files):
    # 获取文件扩展名
    ext = os.path.splitext(file_name)[1]
    
    # 创建6位数的新文件名
    new_num = start_num + i
    new_name = f"{new_num:06d}{ext}"  # :06d 表示6位数字，不足的用0填充
    
    # 构造完整的源文件路径和目标文件路径
    old_file_path = os.path.join(source_folder, file_name)
    new_file_path = os.path.join(target_folder, new_name)
    
    # 将文件复制到目标文件夹并重命名
    shutil.copy2(old_file_path, new_file_path)
    
    print(f"Copied and renamed: {file_name} -> {new_name}")

print(f"\n所有文件已重命名并保存到: {target_folder}")
print(f"处理了 {len(image_files)} 个文件")