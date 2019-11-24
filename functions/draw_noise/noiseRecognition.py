import cv2
import numpy as np 
import matplotlib.pyplot as plt
from random import randint
from random import seed

def main():
    imgBeauty = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\01_Beauty\\Beauty__RenderCamShape_beauty_ID.0001.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    imgGrid = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_Patterns\\GeneratedGrid.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    imgNoisePattern = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_Patterns\\pixelNoisePattern.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    dimensions = imgGrid.shape
    height = imgNoisePattern.shape[0]
    width = imgNoisePattern.shape[1]
    imgBrush = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_Patterns\\Alpha_002.brush_CC0.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    brushHeight = imgBrush.shape[0]
    brushWidth = imgBrush.shape[1]


    # Finding the noise pattern in the imgGrid
    res = cv2.matchTemplate(imgGrid, imgNoisePattern, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    
    # Drawing Rectangles on the locators where the the pattern has been detected
    size = 20
    current = 0
    roiXstart = []
    roiYstart = []
    roiXend = []
    roiYend = []
    # Setting back the grid image to white
    imgGrid[0:1080, 0:1920] = [0.0,0.0,0.0]


    for i in loc[1]:
        # Start and end positions
        startY = (loc[0][current]) - size
        startX = (loc[1][current]) - size
        endY = (startY) + (size * 2)
        endX = (startX) + (size * 2)
        # Drawing Image - Rectangle for debugging purposes
        #cv2.rectangle(imgGrid, (startX, startY),(endX, endY), (1.0,0.0,0.0), 1)
        roiXstart.append(startX)
        roiYstart.append(startY)
        roiXend.append(endX)
        roiYend.append(endY)

        # defining the seed for the random rotation generation
        seed(current)

        # Defining ROI as an image
        roiMain = imgGrid[startY:endY,startX:endX]

        # Resize imgBrush to ROI
        roiBrush = cv2.resize(imgBrush,(roiMain.shape[1], roiMain.shape[0]))
        
        rotation = cv2.getRotationMatrix2D((roiMain.shape[1] / 2, roiMain.shape[0] / 2), randint(0, 360), 1)
        roiBrush = cv2.warpAffine(roiBrush, rotation,(roiMain.shape[1], roiMain.shape[0])) 
        roiMask = roiBrush.copy()

        # Changing the color of the roiBrush to the color of the beauty
        beautyPickColor = imgBeauty[loc[0][current], loc[1][current]]

        # Adds the last roiBrush on top of the roiMain in order to have overlapping brush strokes 
        roi_Computed = roiMain
        # Assigning directly the beautyPickColor in order to avoid adding colors on top of another
        roi_Computed[np.where((roiMask > 0.1).all(axis=2))] = beautyPickColor

        # Place the ROI on a new image size of the grid frame
        imgGrid[startY:endY,startX:endX] = roi_Computed
        
        # Passing onto the next locator
        current += 1
        

    cv2.imshow('Output', imgGrid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\output.exr', imgGrid)


if __name__ == '__main__':
    main()

