import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def main():
    imgGrid = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\GeneratedGrid.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    imgMask = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\Constant_Colors__RenderCamShape_beauty_ID.0001.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    gridMasked = cv2.multiply(imgGrid, imgMask)
    
    cv2.imshow('image', gridMasked)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\_Patterns\\GeneratedGrid.exr', gridMasked)


if __name__ == '__main__':
    main()



