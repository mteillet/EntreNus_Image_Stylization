import cv2
import numpy as np 
import matplotlib.pyplot as plt 

# Takes an ID exr as an input and outputs the masks depending on the values indicated by the redMasking and the lowMasking

def main():
    # Opening EXR file
    imgExr = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\00_ID_Example\\Constant_Colors__RenderCamShape_beauty_ID.0001.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    # Trying to detect Red
    #                    ([B,G,R])
    redMasking = np.array([0.0,.0,1.0])
    lowMasking = np.array([0.0,0.0,0.1])

    mask = cv2.inRange(imgExr, lowMasking, redMasking)

    # Masking the Red
    imgRed = imgExr.copy()
    # Setting IMG to black where mask is none
    imgRed[np.where(mask == 0)] = 0
    # Setting IMG to white where mask is none
    imgRed[np.where(mask != 0)] = 1

    cv2.imshow('image', imgRed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\Constant_Colors__RenderCamShape_beauty_ID.0001.exr', imgRed)

    #return(outID)


if __name__ == '__main__':
    main()

