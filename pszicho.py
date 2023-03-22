import cv2
import json
import os
import sys 
import numpy as np

LOOKUP = {
    (0,0): 'UL',
    (0,1): 'UR',
    (1,0): 'LL',
    (1,1): 'LR'
}

def get_warmness(img):

    # Convert to LAB color space
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Extract the a and b channels
    a_channel = lab_img[:, :, 1]
    b_channel = lab_img[:, :, 2]

    # Calculate the mean values of the a and b channels
    a_mean = np.mean(a_channel)
    b_mean = np.mean(b_channel)
    
#     stddev_a = np.std(a_channel)
#     stddev_b = np.std(b_channel)

    # Calculate the warmness of the image
    warmness = np.sqrt(b_mean**2 + a_mean**2)

    return warmness

if __name__ == '__main__':
    
    input_path = sys.argv[1]
    
    res = {}
    
    for root, subdirs, files in os.walk(input_path):
        for f in files:
            file_path = os.path.join(root,f)
            img = cv2.imread(file_path)
            if img is not None:
                size = int(len(img)/2)
                res[file_path] = {}
                for x in [0,1]:
                    for y in [0,1]:
                        img_part = img[x*size:(x+1)*size, y*size:(y+1)*size]
                        res[file_path][LOOKUP[(x,y)]] = get_warmness(img_part)
                        
    with open('results.json', 'w') as fp:
        json.dump(res, fp)
    