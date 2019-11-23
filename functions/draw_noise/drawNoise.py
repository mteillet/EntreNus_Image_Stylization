import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def main():
    imgExr = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\00_ID_Example\\Constant_Colors__RenderCamShape_beauty_ID.0001.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    dimensions = imgExr.shape
    height = imgExr.shape[0]
    width = imgExr.shape[1]

    #Drawing the noise
    imgNoised = imgExr.copy()
    imgNoised[0:height,0:width] = (0.0,0.0,0.0)
    
    #Setting the distance between each white pixel
    distance = 20
    h0 = 0
    h1 = 1
    w0 = 0
    w1 = 1
    while h1 < height:
        while w1 < width: 
            imgNoised[h0:h1,w0:w1] = (1.0,1.0,1.0)
            w0 += distance
            w1 += distance
        w0 = 0
        w1 = 1
        h0 += distance
        h1 += distance

    
    cv2.imshow('image', imgNoised)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\GeneratedGrid.exr', imgNoised)


if __name__ == '__main__':
    main()

