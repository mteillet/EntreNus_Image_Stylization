import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def main():
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
    size = 70
    current = 0
    roiXstart = []
    roiYstart = []
    roiXend = []
    roiYend = []
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

        # Defining ROI as an image
        roiMain = imgGrid[startY:endY,startX:endX]
        # Resize imgBrush to ROI
        roiBrush = cv2.resize(imgBrush,(roiMain.shape[1], roiMain.shape[0]))

        # Adds the last roiBrush on top of the roiMain in order to have overlapping brush strokes 
        roi_Computed = cv2.add(roiMain, roiBrush)

        # Place the ROI on a new image size of the grid frame
        imgGrid[startY:endY,startX:endX] = roi_Computed
        

        current += 1
        
        


    cv2.imshow('image', imgGrid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\GeneratedGrid.exr', imgNoised)


if __name__ == '__main__':
    main()

