import cv2
import json
import random
import shutil


split = "val"

images_path = f"Desktop/vizwiz-validation/{split}/"
subset_path = f"Desktop/vizwiz-validation/{split}_subset"
json_path = f"Desktop/vizwiz-validation/VizWiz_SOD_{split}_challenge.json"
subset_json_path = f"Desktop/vizwiz-validation/subset_binary_masks.json"

dataset = json.load(
    file := open(json_path, "r")
); file.close()

subset = json.load(
        file2 := open(subset_json_path, "r+")
    )


random.seed()


for entry in dataset:
    if random.randint(0, 10) == 0:
        shutil.copy2(images_path + entry, subset_path)
        subset[entry] = dataset[entry]

json.dump(subset, file2, indent = 4)
file2.close()
    

