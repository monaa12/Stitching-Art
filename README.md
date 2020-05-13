![cover](https://user-images.githubusercontent.com/36296119/81631574-701fc180-9408-11ea-802f-159cab2598cc.png)




# Stitching-Art

## Table of Contents
* [Description](#Description)

* [Features](#Features)

* [Specification](#Specification)

* [Ready to use ?](#Ready-to-use?)

* [Team members](#Team-members)

---

## Description
Cross stitch is a relaxing and rewarding craft.Most cross-stitchers tend to follow a chart with a pre-planned design when attempting a new project, as freehanding an entire design can be unwieldy, and here comes the role of stitching art project. Simply the user can capture a photo and in a glance he will see the cross stitch gridded pattern in front of his eyes. Below is a simple demonstration of the whole process,

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/31513435/81756201-5ab79f80-94bb-11ea-819d-afc43e2d7aee.gif)

---


## Features
### 1) Uploading photo
- The user can uplaod his own photo either From
    * mobile's storage
    * mobile's camera     
### 2) Photo Editing
- The user can crop his own photo either by
    * manual cropping through dragging,zooming in or zooming out
    * automatic cropping through object detection and the user just enter a label for the target object  
### 3) Gridded pattern complexity
- The user can determine the complexity level by
    * Entering the number of stitches in width 
    * Entering the number of colors required where all the colors in the image will be matched to 
- Note: Choosing large number of stitches and/or large number of colors means greater complexity 
### 4) Desgining details
- The user will get the design divided into four main sections
    *  Two gridded images 
      * One with original colors  
      * One with matched DMC colors
    * Note: The first image will be colored with the closest match according to the number of colors enterd by the user and then DMC colors will be chosen based on it 
    * Two pie Charts with percentages and legends
      * One with original colors, it's legend will list the colors in hex
      * One with matched DMC colors, it's legend will list the dmc color CODES and the number of skeins 
    * The number of Skeins
      * Based on matched colors and the percentages provided in the pie chart, the app will compute the number of skeins for each color and list them   in the legend
    * The real dimensions of the design in cm
      * Based on the number of stitches in width entered by the user, the app will compute the required width and height for the design         in cm and plot it as a subtitle below the pie charts  

---

## Specification
-Mobile application creating cross stitching gridded pattern with DMC colors for your chosen image.

-The front-end is in [Flutter](https://flutter.dev) framework.

-The back-end is in [Python 3](https://www.python.org/download/releases/3.0/) using [Flask](http://flask.pocoo.org/) framework.

-The Core project is developed using [OpenCV](https://opencv.org/) , [cvlib](https://www.cvlib.net/) , [matplotlib](https://realpython.com/python-matplotlib-guide/) ,and [pillow](https://python-pillow.org/) libraries.

-The model used for color identification in image is [k-means](https://towardsdatascience.com/k-means-clustering-algorithm-applications-evaluation-methods-and-drawbacks-aa03e644b48a) in python.

---

## Ready to use?
### 1) Download this repo
- From GitHub: Clone or Download the repository or
- From Git:
    > git clone https://github.com/monaa12/Stitching-Art.git

### 2) Frontend launching:
  - Download flutter , android studio and git.

  - Run in flutter terminal in project directory the following command--> flutter packages git.

  - Choose suitable emulator or use physical mobile device.

### 3) Flask launching:
   Run the following commands

   - pip install -r requirements.txt

   - set FLASK_APP= api.py

   - set FLASK_DEBUG= false

   - flask run


---

## Our Team
- [Mona Mahmoud Abdelhafez](https://github.com/monaa12)
- [Menna Tullah Hussein Ali](https://github.com/menna-hussien)
- [Esraa Mohsen Salah](https://github.com/Esraa1moshsen)
- [Haidy Samir Elsayed](https://github.com/HaidySamir1696)
- [Nour Elhoda Ashraf Muhammad](https://github.com/nourelhoda25)

---
