# Importing libraries required for image processing
from collections import Counter

import cv2
import cvlib as cv
import matplotlib.pyplot as plt
import numpy as np
# conversion of dmc colors
import pandas as pd
from PIL import Image
from cvlib.object_detection import draw_bbox
# pie chart
from sklearn.cluster import KMeans

import globals
import os
import math


# conversion of dmc
def conversion_dmc(json_file_path):
    """  Read json file using pandas  .

    Parameters
    ---------
    json_file_path: the path of json file  .

    """
    df = pd.read_json(json_file_path)
    return df


# get the image from frontend
def get_image(image_path):
    """  Get the image and read it using CV2 and convert it to RGB .

    Parameters
    ---------
    image_path: the path of the image .


    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def object_detection(image_path):
    """  Detect the specific object from the image  .

    Parameters
    ---------
    image_path: the path of the image  .

    """

    im = cv2.imread(image_path)
    bbox, labels, conf = cv.detect_common_objects(im, enable_gpu=True)
    # print(bbox[0][0], labels)
    output_image = draw_bbox(im, bbox, labels, conf)
    # plt.imshow(output_image)
    # plt.show()
    # convert the image to be in RGB mode
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(output_image)

    # For reversing the operation
    im_np = np.asarray(im_pil)

    # Shows the image in image viewer
    plt.figure(figsize=(20, 20))
    plt.imshow(im_np)
    plt.savefig(os.path.join(globals.app.static_folder, "show_objects.png"))

    return im_pil, bbox, labels


def crop_object(im_pil, bbox, labels, gb_label):
    """ Crop specific object from the image     .

    Parameters
    ---------
    im_pil: PIL image .

    bbox: the output box created by object detection function

    labels: labels of detected objects in the image

    gb_label: global.label value sent by the user

    """

    # Setting the points for cropped image
    # l = input("please enter the required object: ")
    i = 0
    for x in labels:
        if gb_label == x:
            left = bbox[i][0]
            top = bbox[i][1]
            right = bbox[i][2]
            bottom = bbox[i][3]
            break
        i = i + 1

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im_pil.crop((left, top, right, bottom))

    # For reversing the operation
    im_np = np.asarray(im1)
    return im_np, im1


def RGB2HEX(color):
    """ Convert RGB values to HEX   .

    Parameters
    ---------
    color:  required color in RGB to be converted to HEX

    """
    return "#{:02x}{:02x}{:02x}".format(int(round(color[0])), int(round(color[1])), int(round(color[2])))


def HEX2RGB(color):
    """ Convert HEX values to RGB values   .

    Parameters
    ---------
    color:  required color in HEX to be converted to RGB


    """

    h = color.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def get_colors(image, number_of_colors, show_chart, dmc_df):
    """  Display the 2 pie charts (one for the original color of the image after pixelation and one for DMC color)
         ,Count  number of skeins are needed for each color and  Display the gridded image by specific number
          of colors and DMC colors.

    Parameters
    ---------
    image: PIL image .

    number_of_colors: the number of colors the user wants the image to be converted to.

    show_chart: is taken value True or False to give option for user to show
                the pie chart.

    dmc_df: Dataframe of DMC colors (the json file).


    """

    # Start by pixelating the input images
    image = pixelate(image, globals.no_width_grids)

    # trying to get pixel_size
    pixel_size = int(image.size[0] / globals.no_width_grids)
    image = np.asarray(image)
    modified_image = image.reshape(image.shape[0] * image.shape[1], 3)

    # Start the K-means algorithm to identify all colors into certain number_of_colors given by the user
    clf = KMeans(n_clusters=number_of_colors, n_init=20)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_

    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    dmc_colors_codes = []
    dmc_colors_hex_labels = []
    dmc_colors_rgb = []
    pie_dmc = []
    sorted_counts = list(counts.values())

    for i in range(len(hex_colors)):
        r = int(round(rgb_colors[i][0]))
        g = int(round(rgb_colors[i][1]))
        b = int(round(rgb_colors[i][2]))
        dmc_code, r, g, b, dmc_hex = matchDMC(r, g, b, dmc_df)
        dmc_colors_codes.append("DMC code: " + str(dmc_code))
        dmc_colors_rgb.append([r, g, b])
        dmc_colors_hex_labels.append("#" + dmc_hex.lower())

        # Adding the number of skeins to the pie chart
        pixelate_count = (int(sorted_counts[i] / (pixel_size * pixel_size)))
        list_skeins = ("no of skeins: " + str(math.ceil(pixelate_count / 1493)))
        pie_dmc.append([dmc_colors_codes[i], list_skeins])

    # conversion the color of input_image to the specific no.of colors entered by user
    (h, w) = image.shape[:2]

    # create the new image with DMC colors
    new_image = []

    # looping on each pixel and convert it to DMC color
    for i in range(len(labels)):
        label_color = labels[i]
        r = int(round(dmc_colors_rgb[label_color][0]))
        g = int(round(dmc_colors_rgb[label_color][1]))
        b = int(round(dmc_colors_rgb[label_color][2]))
        new_image.append([r, g, b])

    new = np.reshape(new_image, (h, w, 3))

    # convert the image from np.array to PIL.Image
    img = Image.fromarray(new.astype(np.uint8))

    # converting to gridded_image
    grided_image(img, globals.no_width_grids, 1)

    if show_chart:

        # pie_chart_with_hex_values
        plt.figure(figsize=(12, 10))
        plt.pie(counts.values(), colors=hex_colors, autopct='%1.1f%%')
        plt.title("Original pie chart")
        plt.legend(labels=hex_colors, bbox_to_anchor=(0.85, 1.025), loc='upper left', fontsize=13)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.81)
        plt.tight_layout()
        plt.savefig(os.path.join(globals.app.static_folder, "pie_chart.png"))

        # dmc_pie_chart_with_number_of_skeins
        plt.figure(figsize=(12, 10))
        plt.pie(counts.values(), colors=dmc_colors_hex_labels, autopct='%1.1f%%')
        plt.title("DMC pie chart")
        plt.legend(labels=pie_dmc, bbox_to_anchor=(0.85, 1.025),  loc='upper left', fontsize=13)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.81)
        plt.tight_layout()
        plt.savefig(os.path.join(globals.app.static_folder, "dmc_pie_chart.png"))
    return ""


def pixelate(input_image, no_width_grids):
    """Provides pixelation for image  .

    Parameters
    ---------
    input_image: PIL image.

    no_width_grids: number of stitches of the width .

    """

    (w, h) = input_image.size[:2]
    pixel_size = 10  # initial
    image = input_image  # initial

    if w % no_width_grids != 0:
        # resizing the input_image to fit no_of_grids
        division = math.ceil(w / no_width_grids)
        newsize = (division * no_width_grids, input_image.size[1])
        resized = input_image.resize(newsize)
        image = resized
        pixel_size = int(image.size[0] / no_width_grids)
    else:
        pixel_size = int(w / no_width_grids)

    # pixelating the modified image
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return (image)


def grided_image(input_image, no_width_grids, flag=0):
    """Draw grids according to no. of stitches needed (no_width_grids) .

    Parameters
    ---------
    input_image: PIL image.

    no_width_grids: number of stitches of the width .

    flag (Default = 0) : optional input to give options for input image to be an original image
                         or pixelated image.
    """

    if flag == 1:
        pixelated_image = input_image
    else:
        pixelated_image = pixelate(input_image, no_width_grids)

    # trying to get pixel_size
    pixel_size = int(pixelated_image.size[0] / no_width_grids)

    # getting dimension of pixelated_image
    (w, h) = pixelated_image.size[:2]

    # convert pixelated_image from PIL to np.array
    grided = np.array(pixelated_image)

    # some initializations are used for drawing columns and rows
    size_of_grid_c = pixel_size
    size_of_grid_r = pixel_size
    location_of_row = 0
    location_of_col = 0

    # drawing columns using cv2.line
    for i in range(int(w / pixel_size)):
        location_of_col = location_of_col + size_of_grid_c

        start_point_col = (location_of_col, 0)

        end_point_col = (location_of_col, h)

        color = (0, 0, 0)
        thickness = 1
        grided = cv2.line(grided, start_point_col, end_point_col, color, thickness)

    # drawing rows using cv2.line
    for i in range(int(h / pixel_size)):
        location_of_row = location_of_row + size_of_grid_r

        start_point_row = (0, location_of_row)

        end_point_row = ((w), location_of_row)

        color = (0, 0, 0)
        thickness = 1
        grided = cv2.line(grided, start_point_row, end_point_row, color, thickness)

    # plotting the gridded image
    if flag == 1:
        plt.figure(figsize=(30, 30))
        plt.title("DMC Gridded Pattern", fontsize=80)
        plt.imshow(grided)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.81, hspace=0, wspace=0)
        plt.suptitle("The real dimensions in cm( width:" + str(globals.width) + " ,height:" + str(globals.height) + ")",
                     va='bottom', ha='center', fontsize=40, y=-0.001)
        plt.tight_layout()
        plt.savefig(os.path.join(globals.app.static_folder, "gridded_DMC.png"), bbox_inches='tight',
                    pad_inches=0)

    else:
        plt.figure(figsize=(30, 30))
        plt.title("Original Gridded Pattern", fontsize=80)
        plt.imshow(grided)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.81)
        plt.suptitle("The real dimensions in cm( width:" + str(globals.width) + " ,height:" + str(globals.height) + ")",
                     va='bottom', ha='center', y=-0.001, fontsize=40)
        plt.tight_layout()
        plt.savefig(os.path.join(globals.app.static_folder, "gridded.png"))


def dimension(no_width_grids):
    """Give the dimension of gridded image by cm .

       Parameters
       ---------
       no_width_grids: number of stitches of the width sent by the user.


       """
    image_path = os.path.join(globals.app.config['UPLOAD_FOLDER'], globals.photo.filename)
    image_input = Image.open(image_path)

    # converting the image to pixelated_image
    image = pixelate(image_input, no_width_grids)

    # getting the size of pixel
    pixel_size = int(image.size[0] / no_width_grids)

    # getting the dimension of pixelated image
    (w, h) = image.size[:2]

    # calculating the dimension gridded image by cm
    globals.width = int(w / pixel_size) / 3  # 3 is no. of grids in 1 cm
    globals.height = int(h / pixel_size) / 3  # 3 is no. of grids in 1 cm


def init_app():
    """  the function is used to initialize the image processing phase of the app .
    """

    json_file_path = "./rgb-dmc.json"
    dmc_df = conversion_dmc(json_file_path)
    image_path = os.path.join(globals.app.config['UPLOAD_FOLDER'], globals.photo.filename)

    if globals.obj_flag:
        im_pil, bbox, labels = object_detection(image_path)
        im_np, im_pil = crop_object(im_pil, bbox, labels, globals.label)
        get_colors(im_pil, globals.number_of_colors, True, dmc_df)
        grided_image(im_pil, globals.no_width_grids, 0)
        globals.obj_flag = False

    else:
        image_input = Image.open(image_path)
        get_colors(image_input, globals.number_of_colors, True, dmc_df)
        grided_image(image_input, globals.no_width_grids, 0)

    return ""


def distanceFromColor(idx, r, g, b, dmc_df):
    """ Calculate the distance between r,g,b and a certain color in the dataframe identified by idx  .

    Parameters
    ---------
    idx: the id of the color in the dataframe .

    r: the value of red color.

    g: the value of green color.

    b: the value of blue color.

    dmc_df: the dataframe of DMC colors (json file) .

    """
    tr = dmc_df.loc[idx]['r']
    tg = dmc_df.loc[idx]['g']
    tb = dmc_df.loc[idx]['b']
    
    # calculating the distance between the color given and the target color in the dataframe
    base_distance = ((r - tr) * (r - tr)) + ((g - tg) * (g - tg)) + ((b - tb) * (b - tb))
    distance = math.sqrt(base_distance)
    return distance


def matchDMC(redVal, greenVal, blueVal, dmc_df):
    """  Match DMC color with the color of image  .

    Parameters
    ---------
    redVal:the value of red color  .

    greenVal: the value of green color.

    blueVal: the value of blue color.

    dmc_df: Dataframe of DMC colors .

    """
    distance_list = []

    for idx in range(len(dmc_df)):
        candidate_dist = distanceFromColor(idx, redVal, greenVal, blueVal, dmc_df)
        distance_list.insert(idx, [candidate_dist, idx])
        # To stop looping in case the detecting color already match an existing dmc color
        if candidate_dist == 0:
            dmc_i = dmc_df.loc[idx]['floss']
            dmc_r = dmc_df.loc[idx]['r']
            dmc_g = dmc_df.loc[idx]['g']
            dmc_b = dmc_df.loc[idx]['b']
            hex_i = dmc_df.loc[idx]['hex']
            return dmc_i, dmc_r, dmc_g, dmc_b, hex_i

    # sort the list in ascending order in order to take the shortest distance which is th closest color
    distance_list.sort()

    # Get the values that are closest to the RGB value from first row of {distance_list} and idx column and search in
    # the dataframe to get the color (which is the same id in data frame of dmc colors{dmc_df})
    dmc_i = dmc_df.loc[distance_list[0][1]]['floss']
    dmc_r = dmc_df.loc[distance_list[0][1]]['r']
    dmc_g = dmc_df.loc[distance_list[0][1]]['g']
    dmc_b = dmc_df.loc[distance_list[0][1]]['b']
    hex_i = dmc_df.loc[distance_list[0][1]]['hex']

    # in case we make an option to give three different alternatives for each dmc color
    second_color = dmc_df.loc[distance_list[1][1]]['floss']
    third_color = dmc_df.loc[distance_list[2][1]]['floss']
    fourth_color = dmc_df.loc[distance_list[3][1]]['floss']

    return dmc_i, dmc_r, dmc_g, dmc_b, hex_i

