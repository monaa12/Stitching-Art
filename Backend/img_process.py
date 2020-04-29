# Importing libraries required for image processing
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
from PIL import Image
import numpy as np
#pie chart
from sklearn.cluster import KMeans
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os


def object_detection_cropping(image_name, label):
    im = cv2.imread(image_name)
    bbox, labels, conf = cv.detect_common_objects(im,enable_gpu=True)
    #print(bbox[0][0], labels)
    output_image = draw_bbox(im, bbox, labels, conf)
    #plt.imshow(output_image)
    #plt.show()
    # convert the image to be in RGB mode
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(output_image)

    # Setting the points for cropped image
    #l = input("please enter the required object: ")
    i=0
    for x in labels:
        if label==x:
            left = bbox[i][0]
            top = bbox[i][1]
            right = bbox[i][2]
            bottom = bbox[i][3]
            break
        i = i+1

    # Cropped image of above dimension
    # (It will not change orginal image)
    im1 = im_pil.crop((left, top, right, bottom))

    # For reversing the operation
    im_np = np.asarray(im1)

    #Shows the image in image viewer
    #plt.imshow(im_np)
    #plt.show()
    return im_np

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_colors(image,number_of_colors,show_chart):

    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.savefig("D:/4th year computer/SECOND TERM/image processing/project/implementation/static/pie_char") # save above pie chart with name pie_chart


    return rgb_colors


def resized_image(input_image, width_cm, height_cm):
    # 1cm equivalent 15 pixels
    newsize = (15 * width_cm, 15 * height_cm)
    resized = input_image.resize(newsize)
    return (resized)


def pixelate(resized_image):
    pixel_size = 5  # as each grid is 3 mm and 1 cm with 15 pixel so we made pixel_size with the size of a grid
    image = resized_image
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return (image)


def grided_image(pixelated_image, width_cm, height_cm):
    # drawing rows and columns according to no. of stitches needed
    pixel_size = 5  # size of  a grid
    grided = np.array(pixelated_image)
    print(type(grided))
    size_of_grid = pixel_size
    location_of_row = 0
    location_of_col = 0
    print(size_of_grid)

    # drawing columns
    for i in range(int((15 * width_cm) / (pixel_size))):
        location_of_col = location_of_col + size_of_grid

        start_point_col = (location_of_col, 0)

        end_point_col = (location_of_col, (15 * height_cm))

        color = (105, 105, 105)
        thickness = 1
        grided = cv2.line(grided, start_point_col, end_point_col, color, thickness)
    # drawing rows
    for i in range(int(15 * height_cm / pixel_size)):
        location_of_row = location_of_row + size_of_grid

        start_point_row = (0, location_of_row)

        end_point_row = ((15 * width_cm), location_of_row)

        color = (105, 105, 105)
        thickness = 1
        grided = cv2.line(grided, start_point_row, end_point_row, color, thickness)
    plt.figure(figsize=(20, 20))
    plt.imshow(grided)

#for testing
#image_path = 'D:/4th year computer/SECOND TERM/image processing/project/a&p.PNG'
#label = "apple"
#im_np = object_detection_cropping(image_path, "apple")
#plt.imshow(im_np)
#plt.show()
#get_colors(im_np, 8, True)
#fot testing  grided
#image_input = Image.open(r'C:\Users\Esraa\Videos\real-smile.jpg')
#new_image = resized_image(image_input,16,21)
#pixelated = pixelate(new_image)
#grided_image(pixelated,16,21)
