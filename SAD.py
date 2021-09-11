import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from google.colab.patches import cv2_imshow
import time
from numba import njit

#Set parameters
maxDisparity = 20
window_size = 5
min_delta_sad = 10 

left = np.asanyarray(Image.open('imL.png'))
right = np.asanyarray(Image.open('imR.png')) 

left_img = cv2.cvtColor(np.float32(left),cv.COLOR_RGB2GRAY)
right_img = cv2.cvtColor(np.float32(right),cv.COLOR_RGB2GRAY) 
 
left_img = np.asanyarray(left_img,dtype=np.double)
right_img = np.asanyarray(right_img,dtype=np.double)
img_size = np.shape(left_img)[:2] 
 
plt.imshow(left_img,'gray')
plt.show() 
 
plt.imshow(right_img,'gray')
plt.show() 

@njit(fastmath=True, cache=True)
def calc_sad():
 diff = np.zeros(img_size)
 imgDiff= np.zeros((img_size[0],img_size[1],maxDisparity))
 for i in range(0, maxDisparity):
   diff = np.abs(right_img[:, 0:(img_size[1] - i)] - left_img[:, i: img_size[1]])
   sad = np.zeros(img_size)
   for x in range(blockSize, (img_size[0] - blockSize)):
     for y in range(blockSize, (img_size[1] - blockSize)):
       sad[x, y] = np.sum(diff[(x - blockSize): (x + blockSize), (y  blockSize): (y + blockSize)])
   imgDiff[:,:,i] = sad   
 return imgDiff 

@njit(fastmath=True, cache=True) 
def calc_disp_map():
   disp_map = np.zeros(img_size)
   for x in range(0, img_size[0]):
    for y in range(0, img_size[1]):
     sort = np.sort(imgD[x,y,:])
     if np.abs(sort[0] - sort[1]) > min_delta_sad:
      sort_in = np.argsort(imgD[x,y,:])
      disp_map[x, y] = sort_in[0] / maxDisparity
 return disp_map 

start = time.time()
imgD = calc_sad()
dispMap = calc_disp_map()
end = time.time()
print(time', end - start) 
plt.imshow (dispMap, 'gray') 
plt.show() 
