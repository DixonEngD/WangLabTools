import os
from PIL import Image

def convert_png_to_jpg(folder_path):
    # 获取文件夹中的文件
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"错误：文件夹 {folder_path} 不存在。")
        return

    # 筛选出 PNG 文件
    png_files = [file for file in files if file.lower().endswith('.png')]

    # 转换 PNG 文件为 JPG 文件
    for png_file in png_files:
        png_path = os.path.join(folder_path, png_file)
        jpg_file = os.path.splitext(png_file)[0] + ".jpg"
        jpg_path = os.path.join(folder_path, jpg_file)

        try:
            with Image.open(png_path) as img:
                rgb_img = img.convert('RGB')  # 转换为 RGB 模式
                rgb_img.save(jpg_path, "JPEG")
            print(f"已成功将 {png_file} 转换为 {jpg_file}。")
        except Exception as e:
            print(f"转换 {png_file} 时出错：{e}")

# 示例用法
if __name__ == "__main__":
    folder_path = input("请输入图片文件夹路径：")
    convert_png_to_jpg(folder_path)
