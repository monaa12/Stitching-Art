import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
from numpy import asarray
import glob


def show_images(images, cols=3, titles=None):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 3): Number of columns in figure (number of rows is
                        3).

    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    rows = 3
    assert ((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure(figsize=())
    for n, (image, title) in enumerate(zip(images, titles)):
        # a = fig.add_subplot(rows ,cols , n + 1)
        if n == 0:
            axes1 = fig.add_subplot(rows, cols, 2)
            # axes1   = plt.subplot2grid((3, 3), (0, 1))
            plt.imshow(image)
            axes1.set_title(title)
        elif n == 1:
            axes2 = fig.add_subplot(rows, cols, 5)
            # axes2   = plt.subplot2grid((3, 3), (1, 1))
            plt.imshow(image)
            axes2.set_title(title)
        elif n == 2:
            axes3 = fig.add_subplot(rows, cols, 7)
            # axes3   = plt.subplot2grid((3, 3), (2, 0))
            plt.imshow(image)
            axes3.set_title(title)
        elif n == 3:
            axes4 = fig.add_subplot(rows, cols, 8)
            # axes4   = plt.subplot2grid((3, 3), (2, 1))
            plt.imshow(image)
            axes4.set_title(title)
        else:
            axes5 = fig.add_subplot(rows, cols, 9)
            # axes5   = plt.subplot2grid((3, 3), (2, 2))
            plt.imshow(image)
            axes5.set_title(title)


# fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    # added by me :D just to save the image in the the static folder
    fig.savefig(os.path.join(globals.app.static_folder, "output.png"))


#titles = ["grided_photo", "original_color", "highly_recommended_dmc", "medium_recommended_dmc", "least_recommended_dmc"]
#images = []
#for f in glob.iglob("C:/Users/Esraa/Videos/static/*"):
 #   images.append(np.asarray(Image.open(f)))


#images = np.array(images)
#show_images(images, titles=titles)
