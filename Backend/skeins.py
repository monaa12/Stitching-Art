from sklearn.cluster import KMeans
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from PIL import Image
import pandas as pd
import math


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


def conversion_dmc(json_file_path):
    df = pd.read_json(json_file_path)
    return df


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(round(color[0])), int(round(color[1])), int(round(color[2])))


def HEX2RGB(color):
    h = color.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def get_colors(image, number_of_colors, show_chart, dmc_df, no_width_grids=90):
    # added by esraa
    image = pixelate(image, no_width_grids)

    # trying to get pixel_size
    pixel_size = int(image.size[0] / no_width_grids)
    print(pixel_size)
    plt.figure()
    plt.imshow(image)
    image = np.asarray(image)
    ####
    # modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    # plt.figure()
    # plt.imshow(modified_image)
    modified_image = image.reshape(image.shape[0] * image.shape[1], 3)
    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    # added by esraa
    print("counts=", counts)
    print(type(counts))
    pixelate_count = []
    list_skeins = []
    list_string_skeins = []
    for i in range(int(number_of_colors)):
        pixelate_count.append(int(counts[i] / (pixel_size * pixel_size)))
        list_skeins.append(math.ceil(pixelate_count[i] / 1493))
        list_string_skeins.append("no of skeins :")
    pixelate_count.sort(reverse=True)
    list_skeins.sort(reverse=True)
    print("pixelate_count", pixelate_count)
    print("list_skeins", list_skeins)

    ####
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    ##################
    dmc_colors_codes = []
    dmc_colors_hex_labels = []
    dmc_colors_rgb = []
    for i in range(len(hex_colors)):
        r = int(round(rgb_colors[i][0]))
        g = int(round(rgb_colors[i][1]))
        b = int(round(rgb_colors[i][2]))
        dmc_code, r, g, b, dmc_hex = matchDMC(r, g, b, dmc_df)
        dmc_colors_codes.append(dmc_code)
        dmc_colors_rgb.append([r, g, b])
        dmc_colors_hex_labels.append("#" + dmc_hex.lower())
    ####################

    ###added by esraa
    pie_original = [(hex_colors[i], list_string_skeins[i], list_skeins[i]) for i in range(0, len(hex_colors))]
    # pie_original = [(pie_original_1[i], list_skeins[i]) for i in range(0, len(pie_original_1))]
    pie_dmc = [(dmc_colors_codes[i], list_string_skeins[i], list_skeins[i]) for i in range(0, len(dmc_colors_codes))]
    # pie_dmc = [(pie_dmc_1[i], list_skeins[i]) for i in range(0, len(pie_dmc_1))]
    #####
    if show_chart:
        plt.figure(figsize=(8, 6))
        plt.pie(counts.values(), labels=pie_original, colors=hex_colors)
        # added by esraa
        print("values=", counts.values())
        plt.savefig('C:/Users/Esraa/Videos/static/output_2.png', bbox_inches='tight', dpi=150)
        # plt.savefig(os.path.join(globals.app.static_folder, "pie_chart.png"))

        # dmc_pie_chart
        plt.figure(figsize=(8, 6))
        plt.pie(counts.values(), labels=pie_dmc, colors=dmc_colors_hex_labels)
        # added by esraa
        plt.savefig('C:/Users/Esraa/Videos/static/output.png', bbox_inches='tight', dpi=150)
        # plt.savefig(os.path.join(globals.app.static_folder, "dmc_pie_chart.png"))
    return rgb_colors


def init_app():
    json_file_path = r"C:/Users/Esraa/Music/OS_gui/Stitching-Art/Backend//rgb-dmc.json"
    # test conversion
    dmc_df = conversion_dmc(json_file_path)
    # for testing
    image_path = os.path.join(globals.app.config['UPLOAD_FOLDER'], globals.photo.filename)

    if globals.obj_flag:
        im_pil, bbox, labels = object_detection(image_path)
        im_np, im_pil = crop_object(im_pil, bbox, labels, globals.label)
        get_colors(im_np, globals.number_of_colors, True, dmc_df)
        # new_image = resized_image(im_pil, 16, 21)
        # pixelated = pixelate(im_pil)
        grided_image(im_pil, globals.no_width_grids)

    else:
        im_np = get_image(image_path)
        # im_np = cv2.imread(image_path)
        get_colors(im_np, globals.number_of_colors, True, dmc_df)
        # fot testing  gridded
        image_input = Image.open(image_path)
        # new_image = resized_image(image_input, 16, 21)
        # new_image = resized_image(image_input, globals.width, globals.height)
        # pixelated = pixelate(image_input)
        grided_image(image_input, globals.no_width_grids)

    return ""


def distanceFromColor(idx, r, g, b, dmc_df):
    tr = dmc_df.loc[idx]['r']
    tg = dmc_df.loc[idx]['g']
    tb = dmc_df.loc[idx]['b']

    base_distance = ((r - tr) * (r - tr)) + ((g - tg) * (g - tg)) + ((b - tb) * (b - tb))
    distance = math.sqrt(base_distance)
    return distance


def matchDMC(redVal, greenVal, blueVal, dmc_df):
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

    # sort the list in ascending order
    distance_list.sort()

    # Get the values that are closest to the RGB value from first row of {distance_list} and idx column
    # (which is the same id in data frame of dmc colors{dmc_df})
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


json_file_path = r"C:/Users/Esraa/Music/OS_gui/Stitching-Art/Backend/rgb-dmc.json"
dmc_df = conversion_dmc(json_file_path)
im_np = cv2.imread('C:/Users/Esraa/Music/OS_gui/Stitching-Art/Backend/UPLOAD_FOLDER/butter.jpg')
im_pil = Image.open(r'C:\Users\Esraa\Music\OS_gui\implementation\UPLOAD_FOLDER\butter.jpg')
#take care i use im_pil not im_np
get_colors(im_pil, 5, True, dmc_df)