from PIL import Image
import os

# input and output folders
input_folder = '/mnt/e/data/sy/dxb/2'
output_folder = '/mnt/e/data/sy/dxb/1223434543'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

supported_formats = ('.jpg', '.jpeg', '.png')

# request list of image files
image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)])

print(f"🚀 Found {len(image_files)} images to process.")

for file_name in image_files:
    file_path = os.path.join(input_folder, file_name)
    
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            
            mid_point = width // 2
            
            left_img = img.crop((0, 0, mid_point, height))
            right_img = img.crop((mid_point, 0, width, height))

            # build output file paths
            name_without_ext = os.path.splitext(file_name)[0]
            left_path = os.path.join(output_folder, f'{name_without_ext}_left.png')
            right_path = os.path.join(output_folder, f'{name_without_ext}_right.png')
            
            # save images
            left_img.save(left_path)
            right_img.save(right_path)
            
            print(f"Processed {file_name} ({width}x{height}) -> Split at {mid_point}")
            
    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

print("\n✨ All done!")