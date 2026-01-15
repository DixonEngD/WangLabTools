import json
import os

def convert_json_to_txt(json_file, txt_file):
    # 打开并读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 解析图像的宽度和高度
    img_width = data['imageWidth']
    img_height = data['imageHeight']

    # 解析shape内的标签和坐标
    for shape in data['shapes']:
        if shape['label'] == 'fish-10':
            label = 9
        #label = int(shape['label'])  # 标签，假设需要从0开始的索引
            points = shape['points']
        
            # 计算矩形的x_min, y_min, x_max, y_max
            x_min = min(points[0][0], points[1][0])
            y_min = min(points[0][1], points[1][1])
            x_max = max(points[0][0], points[1][0])
            y_max = max(points[0][1], points[1][1])
        
            # 计算中心点的x, y和宽度高度的归一化值
            x_center = (x_min + x_max) / 2.0 / img_width
            y_center = (y_min + y_max) / 2.0 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height

            # 创建TXT文件内容
            txt_content = f"{label} {x_center} {y_center} {width} {height}\n"

            # 写入TXT文件
            with open(txt_file, 'w') as f_out:
                f_out.write(txt_content)
                
            
def batch_convert_json_to_txt(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录下的所有JSON文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(input_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_dir, txt_filename)

            # 转换每个JSON文件
            convert_json_to_txt(json_path, txt_path)
            print(f"Converted {json_path} to {txt_path}")

# 使用函数，将input_directory中的JSON文件批量转换为output_directory中的TXT文件
input_directory = r'E:\data\cy\cy_fx\10'  # 替换为你的JSON文件所在的目录路径
output_directory = r'E:\data\cy\yolo_cy\9'  # 替换为你想要保存TXT文件的目录路径

batch_convert_json_to_txt(input_directory, output_directory)
