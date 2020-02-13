import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def main():
    print("Starting Shadows Customization...")

    ####    Importing image for scan
    imgExr = frameImport()

    ####    Creating a pixel grid based on the distance input of the function noisedGrid
    #   gridListAll[0] = Pixel X coordinates
    #   gridListAll[1] = Pixel Y coordinates
    imgGrid = noiseGrid(imgExr)        

    #### Compare if the pxListAll contains values corresponding to the gridListAll
    imgMultiplied = cv2.multiply(imgExr, imgGrid)

    ####    Scanning image and returning list of non-black pixels
    #   pxListAll[0] = Pixel X coordinates
    #   pxListAll[1] = Pixel Y coordinates
    pxListAll = frameScan(imgMultiplied)

    # turning the detected grid pixels to white    
    current = 0
    for i in pxListAll[0]:
        imgMultiplied[pxListAll[1][current],pxListAll[0][current]] = (1.0,1.0,1.0)
        current += 1


    # Showing a frame
    cv2.imshow('image', imgMultiplied)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


####    IMG IMPORT
def frameImport():
    # Importing a frame
    imgPath = 'D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_holdoutMattes\\CamShape_holdoutMatte.0100.exr'
    imgExr = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    print("Imported the exr : " + imgPath)
    return(imgExr)

####    GOING THROUGH WHITE PX
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


####    DETECTING THE VALUE OF THE PXs
def scanPxValue(x, y, img):
    pxValue = (img[y, x])
    return(pxValue)


####    DRAWING THE NOISE GRID
def noiseGrid(imgExr):

    print("Beginning to draw the noise grid")

    # Copying the original EXR and filling it with black
    imgGrid = imgExr.copy()
    width = imgGrid.shape[1]
    height = imgGrid.shape[0]
    imgGrid[0:height, 0:width] = (0.0,0.0,0.0)

    # Adding the actual noise in the Image
    #Setting the distance between each white pixel
    distance = 5
    gridListX = []
    gridListY = []
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

if __name__ == "__main__":
    main()