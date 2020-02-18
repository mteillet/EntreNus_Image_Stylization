# Python_OpenExr_Stylization
 Images Processing in Python aimed towards stylization of 3D rendering passes

# Install
The following have to be installed :

# Python 3.7+

# OpenCV
"pip install opencv-python"
# Matplotlib
"pip install matplotlib"
# pyQt5
"pip install pyqt5"

# How it works
The program needs a renderpass in openEXR format, 32 bits. It generates a grid of pixels with its density defined by the user. It then colorpicks the actual color of the render pass under each pixel. It loads a brush chosen by the user, and then applies random rotation and user-defined random offset on the brush for each pixel on the grid. Finally it puts the brush instances on the grid, taking into account the color-picked colored previously chosen.

# Example
Here is some examples of what you can get with different inputs - here based on an holdoutmatte pass from renderman:

![](/_exampleGif/Test_v0_001.gif)