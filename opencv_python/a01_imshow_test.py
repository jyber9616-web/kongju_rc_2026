#pip install opencv-python
#pip install numpy
#sudo apt install x11-apps
import cv2
import numpy as np


def main():
    print(cv2.__version__)
    img = np.zeros((400, 600)) #imshow 이미지를 가지고 오는거
    
    cv2.imshow("img", img)
    cv2.waitKey()

if __name__ == "__main__":
    main()