# Informations
This repository contains code produced for the Entre Nus project done at ESMA Nantes school.
It is aimed for the stylization of 3D rendering passes based on the input and brush alphas.
You should use the blinkscripts in nuke if possible, as we had time to develop a lot more of them since the start of production, and they will allow a lot more diversity and tweaking on your images, as well as being quicker to execute than the python script which was only meant as a proof of concept. 

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

# Acknowledgements
Thanks a lot to the ESMA staff for encouraging us to pursue this experimentation path despit the tight deadlines. Special thanks to Leo Columbier for introducing us to blinkscript in Nuke by showing us how to translate our first python mockup to blinkscript.