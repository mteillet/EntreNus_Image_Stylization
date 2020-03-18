# Informations
This repository contains code produced for the Entre Nus project done at ESMA Nantes school.
It is aimed for the stylization of 3D rendering passes based on the input and brush alphas.
You should use the blinkscripts in nuke if possible, as we had time to develop a lot more of them since the start of production, and they will allow a lot more diversity and tweaking on your images, as well as being quicker to execute than the python script which was only meant as a proof of concept. 


# Nuke Blinkscripts

# GridGenerator.cpp
The GridGenerator.cpp is aimed to be used in order to get control the density of the brushes generation and position. For a more natural look, we recommend using an iDistort node on it with an animated noise in order to have a more "flowing" effect. The resulting distorted image should be merged via multiply operation on top of the image you want to generate brushes on
# BrushGenerator_Flat.cpp
The BrushGenerator_Flat.cpp generated brushes on top of your input, keeping the input color, where the value of the input is greater than 0.0f it makes sur the lighter brushes are kept on top of the darker ones.
# BrushGenerator_Nrm.cpp
The BrushGenerator_Nrm.cpp generates brushes in the same manner as the BrushGenerator_Flat.cpp. The only difference is it takes the normal pass of your renders in order to scale down the brushes when the Z (blue) value of your NRM pass is greater than 0. It allows to have a better conservation of the edges and volumes of your renders. When the camera is straight. - The best method would to get the camera vector and use a dot product between the camera vector and the normal pass vector of each pixels, which should soon be coming in another node.
# BrushGenerator_CamVector.cpp
The BrushGenerator_CamVector.cpp generates brushes in the same manner as the previous ones, but it takes a vector input (ideally your camera's) in order to scale the brushes depending on their facing ratio to the camera. You can run BrushGenerator_CamVector_GetVector.py in your maya scene with your camera selected in order to get its current vector and input it into the node in Nuke. You can tweak the scaling of the brushes by altering the values you have entered.


# Python_Standalone version
# Install
The following have to be installed :
# Python 3.7+
https://www.python.org/downloads/release/python-377/
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