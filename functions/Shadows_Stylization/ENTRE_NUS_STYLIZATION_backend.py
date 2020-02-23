import cv2
import numpy as np 
import matplotlib.pyplot as plt 
from random import seed
from random import randint

def entreNusStylization(exrJson, brushJson, brushSizeJson, brushOffsetJson, gridDensityJson):
    print("backend function call")
    # Import image for scan
    imgExr = imgImport(exrJson)

    # Creating the pixel grid
    imgGrid = noiseGrid(imgExr, gridDensityJson)
    
    # Multiplying the grid over the imgExr 
    imgMultiplied = cv2.multiply(imgExr, imgGrid)
    
    # Scanning the pixels for non black ones
    pxListAll = frameScan(imgMultiplied)

    #▲ Turning non white pixels to white in order to run reconnaissance algorithm on the img Multiplied
    imgMultiplied = visualizePixels(pxListAll, imgMultiplied)
    
    # Printing the number of pixels containing information for brush drawing
    locList = noiseDetection(imgMultiplied, imgExr)
    print((str(len(locList[1]))), " pixels were detected as reference points for brush drawing stylization")
    
    imgBrushed = drawBrush(locList, imgExr, brushSizeJson, brushOffsetJson)
    
    return(imgBrushed)
    
def imgImport(exrJson):
    imgPath = exrJson
    imgExr = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    print("Imported the exr : " + imgPath)
    return(imgExr)

def noiseGrid(imgExr, gridDensityJson):
    print("Beginning to draw the noise grid")

    # Copying the original EXR and filling it with black
    imgGrid = imgExr.copy()
    width = imgGrid.shape[1]
    height = imgGrid.shape[0]
    imgGrid[0:height, 0:width] = (0.0,0.0,0.0)

    # Adding the actual noise in the Image
    #Setting the distance between each white pixel
    distance = int(gridDensityJson)
    h0 = 0
    h1 = 1
    w0 = 0
    w1 = 1
    while h1 < height:
        while w1 < width: 
            imgGrid[h0:h1,w0:w1] = (1.0,1.0,1.0)
            w0 += distance
            w1 += distance
        w0 = 0
        w1 = 1
        h0 += distance
        h1 += distance

    return(imgGrid)

def frameScan(imgExr):
    # Scanning the image to detect where the pixel value is above 0
    width = imgExr.shape[1] 
    height = imgExr.shape[0] 
    
    ####    LINE SCANNING   ####
    pixelWidthCount = 0
    pixelHeightCount = 0
    pxListX = []
    pxListY = []

    # Scaning row by row the pixel value of the image (takes some time)
    print("Scanning pixel data (this might take some time)...")
    for i in range(width):
        for i in range(height):
            #print(str(pixelHeightCount) + ":" + str(pixelWidthCount))
            pxValue = scanPxValue(pixelWidthCount, pixelHeightCount, imgExr)
            
            # Check if the pxValue is above 0 or not
            if pxValue[0] != 0 :
                pxListX.append(pixelWidthCount)
                pxListY.append(pixelHeightCount)
     

            pixelHeightCount += 1
        pixelHeightCount = 0
        pixelWidthCount += 1

    print("Pixel scanning completed !")
    print(str(len(pxListX)) + " pixels were detected as containing shadow information")
    return(pxListX, pxListY)

def scanPxValue(x, y, img):
    pxValue = (img[y, x])
    return(pxValue)

def visualizePixels(pxListAll, imgMultiplied):
    current = 0
    for i in pxListAll[0]:
        imgMultiplied[pxListAll[1][current],pxListAll[0][current]] = (1.0,1.0,1.0)
        current += 1
    return(imgMultiplied)

def noiseDetection(imgMultiplied, imgExr):
    print("Beginning to identify noise pixel data")
    imgBrushed = imgMultiplied.copy()
    imgHeight = imgBrushed.shape[0]
    imgWidth = imgBrushed.shape[1]


    # Loading white pixel detection pattern
    imgWhitePx = cv2.imread('pixelNoisePattern.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    # Findng the noise pattern in the imgGrid
    res = cv2.matchTemplate(imgMultiplied, imgWhitePx, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    # loc is containing 2 lists of arrays representing the x and y coordinates of the matches for the white pixel detection
    loc = np.where(res >= threshold)
    print(str(len(loc[1])) + " pixels matches were detected on white pixels recognition")

    # Drawing rectangles on matches of the match template operation
    ####    ROI INITIALIZATION  ####
    print("starting ROI Drawing")
    roiXstart = []
    roiYstart = []
    current = 0

    for i in loc[1]:
        # Start and end positions
        startY = (loc[0][current])
        startX = (loc[1][current])
        # Drawing Image - Rectangle for debugging purposes
        #cv2.rectangle(imgWhitePx, (startX, startY),(endX, endY), (1.0,0.0,0.0), 1)

        roiXstart.append(startX)
        roiYstart.append(startY)
        current += 1

    return(roiXstart, roiYstart)

def drawBrush(locList, imgExr, brushSizeJson, brushOffsetJson):
    print("Begginning the brush drawing proccess...")
    
    brushSize = int(brushSizeJson)
    
    ####    CHECKING FOR OUT OF BORDER PIXELS - They are returned in this state:
    #   checkedList[0] = start X
    #   checkedList[1] = end X
    #   checkedList[2] = start Y
    #   checkedList[3] = end Y
    #   checkedList[4] = random rotation assigned to the point index
    #   checkedList[5] = random offset assigned to the point index
    checkedList = checkBrushSize(brushSize, locList, imgExr, brushOffsetJson)

    placeholderIMG = roiDrawing(checkedList, imgExr, brushSize)
    return(placeholderIMG)

def checkBrushSize(brushSize, locList, imgExr, brushOffsetJson):
    checkedListStartX = []
    checkedListStartY = []
    checkedListEndX = []
    checkedListEndY = []
    randomOffsetList = []
    randomRotList = []
    current = 0
    randomOffset = int(brushOffsetJson)

    print("Checking brush size for out of bounds pixels")
    for i in locList[0]:

        startX = locList[0][current] - int(brushSize) / 2
        startY = locList[1][current] - int(brushSize) / 2
        endX = locList[0][current] + int(brushSize) / 2
        endY = locList[1][current] + int(brushSize) / 2
        if 0 <= startY <= imgExr.shape[0]:
            if 0 <= startX <= imgExr.shape[1]:
                if 0 <= endY <= imgExr.shape[0]:
                    if 0 <= endX <= imgExr.shape[1]:
                        checkedListStartX.append(startX)
                        checkedListStartY.append(startY)
                        checkedListEndX.append(endX)
                        checkedListEndY.append(endY)
                        randomRotList.append(randint(0,360))
                        randomOffsetList.append((randint(0, randomOffset)) - (randomOffset / 2))
        current += 1
    print(str(len(checkedListStartX)), "pixels were kept as usable for brush drawing out of", str(len(locList[0])))
    return(checkedListStartX, checkedListEndX, checkedListStartY, checkedListEndY, randomRotList, randomOffsetList)

def roiDrawing(checkedList, imgExr, brushSize):
    print("Starting to Sample the grid pixels...")
    # Making a black placeholder image before starting to draw the ROIs on it
    placeholderIMG = imgExr.copy()
    placeholderIMG[0:imgExr.shape[0], 0:imgExr.shape[1]] = [0.0,0.0,0.0]
    colorPickList = []

    # Importing the brush alpha
    #D:\00_3D\_GITHUB\Python_3D_IMG_Processing\Inputs\_holdoutMattes
    brushAlpha = cv2.imread('D:\\00_3D\\01_PROJECTS\\01_PRO\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_Patterns\\Alpha_002.brush_CC0.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    #### Detecting and color picking the ROIs returning a colorpicking list which needs to be reordered according to value
    colorPickList = colorPicking(checkedList, brushAlpha, placeholderIMG, colorPickList, imgExr)

    #### Returned zipped lists are as follow :
    #zippedLists[current][0] = colorPickList[current]
    #zippedLists[current][1] = checkedList[0][current]
    #zippedLists[current][2] = checkedList[1][current]
    #zippedLists[current][3] = checkedList[2][current]
    #zippedLists[current][4] = checkedList[3][current]
    #zippedLists[current][5] = checkedList[4][current]
    #zippedLists[current][6] = checkedList[5][current]
    zippedLists = reorderList(checkedList, colorPickList)

    placeholderIMG = brushDrawing(zippedLists, brushAlpha, placeholderIMG, colorPickList, imgExr)

    return(placeholderIMG)

def colorPicking(checkedList, brushAlpha, placeholderIMG, colorPickList, imgExr):
    print("Start color picking the grid Pixels...")
    current = 0
    for i in checkedList[0]:
        #### Uncomment the following line if you need to print the pixel coordinates for the brushes
        #print(checkedList[0][current],checkedList[1][current],checkedList[2][current],checkedList[3][current])

        # Adding the offset to the bounding boxes of the ROIs
        offsetXstart = (int(checkedList[0][current]) + int(checkedList[5][current]))
        offsetXend = (int(checkedList[1][current]) + int(checkedList[5][current]))
        offsetYstart = (int(checkedList[2][current]) + int(checkedList[5][current]))
        offsetYend = (int(checkedList[3][current]) + int(checkedList[5][current]))


        # Defining the bounding box of the brush
        roiBox = placeholderIMG[offsetYstart:offsetYend, offsetXstart:offsetXend]


        # Resize brush alpha to the roiBox size        
        roiBrush = cv2.resize(brushAlpha,(roiBox.shape[1], roiBox.shape[0]))

        
        # Uncomment and use these functions (need to change inputs ofc) if a random rotation is input befor the resize of the roi
        rotation = cv2.getRotationMatrix2D((roiBrush.shape[1] / 2, roiBrush.shape[0] / 2), checkedList[4][current], 1)
        roiBrush = cv2.warpAffine(roiBrush, rotation,(roiBox.shape[1], roiBox.shape[0])) 
        roiMask = roiBrush.copy()

        # Picking the color from the original EXR in order to give it to the brush
        # First, need to go back to the original picked pixel on X and Y coordinates
        locX = (int(checkedList[0][current]) + int(checkedList[1][current])) / 2
        locY = (int(checkedList[2][current]) + int(checkedList[3][current])) / 2
        # Then pick the color
        #       Might need to normalize the value of the exr before picking the value
        colorPick = imgExr[int(locY), int(locX)]
        colorPickList.append(((float(colorPick[0]) + float(colorPick[1]) + float(colorPick[2]))/3.0))
        
        current += 1
    return(colorPickList)

def reorderList(checkedList, colorPickList):
    print("Re-ordering ", str(len(colorPickList)), "pixels based on luminance...")

    current = 0
    #### Zipping the different lists together before sorting - allowing us to sort all list according to the colorpicking values
    zippedLists = list(zip(colorPickList, checkedList[0], checkedList[1], checkedList[2], checkedList[3], checkedList[4], checkedList[5]))
    # Sorting the list of lists
    zippedLists.sort()

    print("Pixels re-ordering completed !")
    return(zippedLists)

def brushDrawing(zippedLists, brushAlpha, placeholderIMG, colorPickList, imgExr):
    print("Starting to draw brushes on the luminance re-ordered ROIs...")
    
    ActualColorList = []
    current = 0
    for i in zippedLists:
        #### Uncomment the following line if you need to print the pixel coordinates for the brushes
        #print(checkedList[0][current],checkedList[1][current],checkedList[2][current],checkedList[3][current])

        # Adding the offset to the bounding boxes of the ROIs
        offsetXstart = (int(zippedLists[current][1]) + int(zippedLists[current][6]))
        offsetXend = (int(zippedLists[current][2]) + int(zippedLists[current][6]))
        offsetYstart = (int(zippedLists[current][3]) + int(zippedLists[current][6]))
        offsetYend = (int(zippedLists[current][4]) + int(zippedLists[current][6]))


        # Defining the bounding box of the brush
        roiBox = placeholderIMG[offsetYstart:offsetYend, offsetXstart:offsetXend]

        # Resize brush alpha to the roiBox size        
        roiBrush = cv2.resize(brushAlpha,(roiBox.shape[1], roiBox.shape[0]))

        
        # Uncomment and use these functions (need to change inputs ofc) if a random rotation is input befor the resize of the roi
        rotation = cv2.getRotationMatrix2D((roiBrush.shape[1] / 2, roiBrush.shape[0] / 2), zippedLists[current][5], 1)
        roiBrush = cv2.warpAffine(roiBrush, rotation,(roiBox.shape[1], roiBox.shape[0])) 
        roiMask = roiBrush.copy()

        # Picking the color from the original EXR in order to give it to the brush
        # First, need to go back to the original picked pixel on X and Y coordinates
        locX = (int(zippedLists[current][1]) + int(zippedLists[current][2])) / 2
        locY = (int(zippedLists[current][3]) + int(zippedLists[current][4])) / 2

        colorPick = imgExr[int(locY), int(locX)]
        ActualColorList.append(((float(colorPick[0]) + float(colorPick[1]) + float(colorPick[2]))/3.0))
        
        roiComputed = roiBox

        # Replacing the color of the roiMask with the colorPicked one
        roiComputed[np.where((roiMask > 0.1).all(axis = 2))] = ActualColorList[current]

        # Placing the roi on the image
        placeholderIMG[offsetYstart:offsetYend, offsetXstart:offsetXend] = roiComputed

        current += 1

    print("ROI drawing completed !")
    return(placeholderIMG)


if __name__ == "__entreNusStylization__":
    entreNusStylization()