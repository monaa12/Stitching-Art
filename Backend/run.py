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


# conversion of dmc
def conversion_dmc(json_file_path):
    df = pd.read_json(json_file_path)
    return df


def object_detection(image_path):
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
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_colors(image, number_of_colors, show_chart, dmc_df):
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    # print(hex_colors)
    ##################
    # print(dmc_df["floss"][1])
    dmc_colors = []
    print(dmc_df.shape)
    for i in range(len(hex_colors)):
        for j in range(1, 454):
            if (dmc_df["hex"][j] == (hex_colors[i].upper())):
                dmc_colors.append(dmc_df["floss"][j])
                print(dmc_colors)

    ####################
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if show_chart:
        plt.figure(figsize=(8, 6))
        plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)
        # plt.savefig("D:/4th year computer/SECOND TERM/image processing/project/implementation/static/pie_chart")  # save above pie chart with name pie_chart
        plt.savefig(os.path.join(globals.app.static_folder, "pie_chart.png"))
    return rgb_colors


def resized_image(input_image, width_cm, height_cm):
    # 1cm equivalent 15 pixels
    newsize = (15 * width_cm, 15 * height_cm)
    resized = input_image.resize(newsize)
    return (resized)


def pixelate(input_image, no_width_grids):
    (w, h) = input_image.size[:2]
    pixel_size = 10  # initial
    image = input_image  # initial
    if w % no_width_grids != 0:
        # resize image to fit no_of_grids
        division = math.ceil(w / no_width_grids)
        newsize = (division * no_width_grids, input_image.size[1])
        resized = input_image.resize(newsize)
        image = resized
        (we, he) = image.size[:2]
        print(we)
        print(he)
        pixel_size = int(image.size[0] / no_width_grids)
    else:
        pixel_size = int(w / no_width_grids)

    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return (image)


def grided_image(input_image, no_width_grids):
    # this function is drawing grids according to no. of stitches needed (no_width_grids)

    # first use the pixelate function to convert the input_impage into pixelated_image
    pixelated_image = pixelate(input_image, no_width_grids)

    # trying to get pixel_size
    pixel_size = int(pixelated_image.size[0] / no_width_grids)
    (w, h) = pixelated_image.size[:2]
    grided = np.array(pixelated_image)
    print(type(grided))
    size_of_grid_c = pixel_size
    size_of_grid_r = pixel_size
    location_of_row = 0
    location_of_col = 0
    #######here the height and width calculationsss
    #getting size of etamin in cm
    globals.width = int((w)/(pixel_size)) / 3 # 3 is no. of grids in 1 cm
    globals.height = int(h/pixel_size) / 3    # 3 is no. of grids in 1 cm
    ################
    # drawing columns
    for i in range(int((w) / (pixel_size))):
        location_of_col = location_of_col + size_of_grid_c

        start_point_col = (location_of_col, 0)

        end_point_col = (location_of_col, (h))

        color = (0, 0, 0)
        thickness = 1
        grided = cv2.line(grided, start_point_col, end_point_col, color, thickness)
        # drawing rows
    for i in range(int(h / pixel_size)):
        location_of_row = location_of_row + size_of_grid_r

        start_point_row = (0, location_of_row)

        end_point_row = ((w), location_of_row)

        color = (0, 0, 0)
        thickness = 1
        grided = cv2.line(grided, start_point_row, end_point_row, color, thickness)
    plt.figure(figsize=(30, 30))
    plt.imshow(grided)
    # plt.savefig("D:/4th year computer/SECOND TERM/image processing/project/implementation/static/grided")
    plt.savefig(os.path.join(globals.app.static_folder, "grided.png"))


def init_app():
    # for testing
    image_path = os.path.join(globals.app.config['UPLOAD_FOLDER'], globals.photo.filename)
    json_file_path = "./rgb-dmc.json"
    # test conversion
    dmc_df = conversion_dmc(json_file_path)

    if globals.obj_flag:
        im_pil, bbox, labels = object_detection(image_path)
        im_np, im_pil = crop_object(im_pil, bbox, labels, globals.label)
        # plt.imshow(im_np)
        # plt.show()
        get_colors(im_np, 8, True, dmc_df)
        new_image = resized_image(im_pil, 16, 21)
        pixelated = pixelate(new_image)
        grided_image(pixelated, 16, 21)

    else:
        im_np = cv2.imread(image_path)
        get_colors(im_np, 8, True, dmc_df)
        # fot testing  gridded
        image_input = Image.open(image_path)
        # new_image = resized_image(image_input, 16, 21)
        new_image = resized_image(image_input, globals.width, globals.height)
        pixelated = pixelate(new_image)
        # grided = grided_image(pixelated, 16, 21)
        grided_image(pixelated, globals.width, globals.height)

    return ""