import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
from numpy import asarray
import glob


def show_images(images, cols=1, titles=None):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 3): Number of columns in figure (number of rows is
                        3).

    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    rows = 2
    assert ((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure(figsize=(30, 30))
    for n, (image, title) in enumerate(zip(images, titles)):
        # a = fig.add_subplot(rows ,cols , n + 1)
        if n == 0:
            axes1 = fig.add_subplot(rows, cols, 1)
            # axes1   = plt.subplot2grid((3, 3), (0, 1))
            plt.imshow(image)
            axes1.set_title(title)
        elif n == 1:
            axes2 = fig.add_subplot(rows, cols, 2)
            # axes2   = plt.subplot2grid((3, 3), (1, 1))
            plt.imshow(image)
            axes2.set_title(title)

    fig.savefig('C:/Users/Esraa/Videos/static/output.png', bbox_inches='tight', dpi=150)
    plt.show()

    ##added by me :D just to save the image in the the static folder
    # plt.savefig(os.path.join(globals.app.static_folder, "output.png"))


titles = ["grided_photo", "highly_recommended_dmc"]
images = []
for f in glob.iglob("C:/Users/Esraa/Videos/static/*"):
    images.append(np.asarray(Image.open(f)))

images = np.array(images)
show_images(images, titles=titles)
