import cv2 as cv
import numpy as np

import random

image = cv.imread('sample4.png', 0)
shap=image.shape
cv.imshow('Original Image',image)
image=cv.resize(image,(int(shap[1]),int(shap[0])))
image_shape, image = cv.threshold(image, 127, 255, 0)
label = 0
image = np.pad(image, ((1, 1), (1, 1)))
label_matrix = np.zeros((image.shape[0], image.shape[1]), np.uint8)

def replace(image,myvalues):
    image[image==max(myvalues)]=min(myvalues)
    return image

for i in range(1,image.shape[0]):
    for j in range(1,image.shape[1]):
        if image[i][j]==255:
            if image[i-1][j]==0 and image[i][j-1]==0:
                label+=1
                label_matrix[i][j]=np.array(label).astype(np.uint8)
            elif image[i-1][j]==0 and image[i][j-1]!=0:
                label_matrix[i][j]=label_matrix[i][j-1]
            elif image[i-1][j]!=0 and image[i][j-1]==0:
                label_matrix[i][j]=label_matrix[i-1][j]
            elif image[i-1][j]!=0 and image[i][j-1]!=0:
                label_matrix[i][j]=min(label_matrix[i-1][j],label_matrix[i][j-1])
  
for i in range(1, label_matrix.shape[0]):
    for j in range(1, label_matrix.shape[1]):
        if label_matrix[i-1][j]!=0 and label_matrix[i][j]!=0:
            label_matrix=replace(label_matrix,(label_matrix[i-1][j],label_matrix[i][j]))
            label-=1
        if label_matrix[i][j-1]!=0 and label_matrix[i][j]!=0:
            label_matrix=replace(label_matrix,(label_matrix[i][j],label_matrix[i][j-1]))
            label-=1
label=[]
for i in range(1, label_matrix.shape[0]):
    for j in range(1, label_matrix.shape[1]):
        if label_matrix[i][j]!=0:
            if len(label)==0:
                label.append(label_matrix[i][j])
            if label_matrix[i][j] in label:
                continue
            else:
                label.append(label_matrix[i][j])
print('Number of Objects are=',len(label))
image=np.zeros((label_matrix.shape[0],label_matrix.shape[1],3),np.uint8)
color=[]
for i in label:
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    color.append((b,g,r))

for i in range(label_matrix.shape[0]):
    for j in range(label_matrix.shape[1]):
      
       if (label_matrix[i][j] in label):
         image[i][j]=color[int(np.where(label==label_matrix[i][j])[0])]
cv.imshow('Objects in Image',image)
cv.waitKey()
