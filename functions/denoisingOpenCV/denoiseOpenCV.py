import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def main():
    imgExr = cv2.imread('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Inputs\\01_Beauty\\Beauty_v001_t01\\Beauty__RenderCamShape_beauty_ID.0001.exr', cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    blur = cv2.bilateralFilter(imgExr, 9, 75, 75)

    cv2.imshow('image', blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #outID = cv2.imwrite('D:\\00_3D\\_GITHUB\\Python_3D_IMG_Processing\\Outputs\\00_ID_Example_out\\Constant_Colors__RenderCamShape_beauty_ID.0001.exr', imgRed)


if __name__ == '__main__':
    main()

