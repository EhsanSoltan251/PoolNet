"""
The following example code loops through all the images in the specified dataset
split, creates a binary ground truth mask of each image, and then appends the 
binary ground truth mask to a list. The mask list can then be used for model 
training, analysis, and other tasks.

Participants can set 'write_binary_masks' to True to write the binary mask as 
an 8-bit PNG per the challenge's submission requirements. Ensure to update the 
path as needed. This code assumes the JSON files and image directories are 
stored at the root level of the project directory. 

Final submissions for binary ground truth masks must be of dimensions 720 x 720.
"""
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt
import os


sizes = []
image_sizes = []
points = []
polygons = []
contrasts = []

print("###################")
print(os.getcwd())

def getBinaryMasks():
    # Change split to "val" or "train" to work on different split. 
    split = "val"

    #images_path = f"Desktop/vizwiz-validation/{split}/"
    #json_path = f"Desktop/vizwiz-validation/VizWiz_SOD_{split}_challenge.json"
    images_path = f"Desktop/vizwiz-validation/val_subset/"
    json_path = f"Desktop/vizwiz-validation/subset_binary_masks.json"


    # Change to True to write binary masks as 8-bit PNG files
    write_binary_masks = True

    dataset = json.load(
        file := open(json_path, "r")
    ); file.close()

    binary_mask_list = []


    for image in dataset:
        original_image = cv2.imread(images_path + image)
        json_resized_dimensions = dataset[image]["Ground Truth Dimensions"]

        # Get dimensions of original image and resized image from JSON data
        original_dimensions = original_image.shape
        original_height = int(original_dimensions[0])
        original_width = int(original_dimensions[1])
        resized_height = json_resized_dimensions[0]
        resized_width = json_resized_dimensions[1]

        

        # Resize image to match JSON data
        resized_image = cv2.resize(
            original_image,
            [resized_width, resized_height],
            interpolation = cv2.INTER_AREA
        )

        # Assert resized image dimensions matches JSON data and create stencil
        resized_dimensions = [resized_image.shape[0], resized_image.shape[1]]
        assert resized_dimensions == json_resized_dimensions
        stencil = np.zeros(resized_dimensions, dtype = np.uint8)
        full_screen = dataset[image]["Full Screen"]

        # If the salient object is full screen then invert the stencil
        if full_screen:
            mask = cv2.bitwise_not(stencil)
        
        # Otherwise create a binary mask of the salient object
        else:
            color = [255, 255, 255]
            salient_object_points = dataset[image]["Salient Object"]
            numpy_list = [np.array(polygon) for polygon in salient_object_points]
            mask = cv2.fillPoly(stencil, numpy_list, color)





            #plotting label characteristics
            sizes.append(cv2.countNonZero(mask)) #want the number of white pixels
            points.append(len(salient_object_points[0]))
            polygons.append(len(salient_object_points))
            image_sizes.append(original_height * original_width)

            c = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
            contrasts.append(c.std())
            
            


        
        # Append binary mask to binary mask list
        binary_mask_list.append(mask)
        
        # Write PNG files if write_binary_masks = True
        if write_binary_masks:
            cv2.imwrite(f"Desktop/vizwiz-validation/masks/" + image[0:-3] + "png", mask)



getBinaryMasks()

'''
#plot the size of binary masks
plt.hist(sizes, bins=50)
plt.xlabel("Size of binary mask")
plt.ylabel("Number of images")
plt.show()


#plot the number of points in binary masks
plt.hist(points, bins=50)
plt.xlabel("Number of points in binary mask polygon")
plt.ylabel("Number of images")
plt.show()

#plot the number of polygons in binary mask
plt.hist(polygons, bins=50)
plt.xlabel("Number of polygons in binary mask")
plt.ylabel("Number of images")
plt.show()

#plot the original size of images
plt.hist(image_sizes, bins=50)
plt.xlabel("Size of image")
plt.ylabel("Number of images")
plt.show()

#plot the constrasts
plt.hist(contrasts, bins=50)
plt.xlabel("RMS Contrast")
plt.ylabel("Number of images")
plt.show()


print("min size: " + str(min(sizes)) + ", max size: " + str(max(sizes)) + "\n")
print("min points: " + str(min(points)) + ", max points: " + str(max(points)) + "\n")
print("min polygons: " + str(min(polygons)) + ", max polygons: " + str(max(polygons)) + "\n")
#print("min original image size: " + str(min(image_sizes)) + ", max size: " + str(min(image_sizes)) + "\n")
'''