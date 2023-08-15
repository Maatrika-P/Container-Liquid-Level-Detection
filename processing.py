import cv2
import numpy as np
import matplotlib.pyplot as pl 

def imshow(title = "", image = None, size =5):
    w= image.shape[0]
    h=image.shape[1]
    aspect_ratio = w/h     
    pl.figure(figsize = (size*aspect_ratio,size))
    pl.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pl.title(title)
    pl.show()

def Colored_Liquid(image):
    im = cv2.imread(image)

    img = cv2.resize(im, (800,1000))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0) #take out noise 

    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) #thresh to separate water from background

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE) #contours of the water 

    max_contour = max(contours, key=cv2.contourArea) #biggest area in water 


    #cv2.drawContours(img, [max_contour], -1, (0, 0, 255), 4) #contour on org img 

    distance = max_contour[0][0][1]  #distance from top of bottle to the level 

    cv2.line(img, (0, distance), (img.shape[1], distance), (0, 255, 0), 2) #draw line on water level 
    cv2.line(img, (0,300), (800,300),(0,255,0), 2) 


    dist_ance = ((distance - 250)/distance)*100
    rounded = round(dist_ance,2)
    hello = print("The percentage of empty part is ", rounded)

    x_axis = int(2*(0 + img.shape[1])/5.5)

    cv2.putText(img,  "percentage of empty = " + str(rounded), (x_axis, distance-100),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1) 

    if rounded < 10:
        return [img, 'Accepted']
    
    elif rounded < 0:
        return [img, 'Overflow']
    
    else:
        return [img, 'Underflow']
    
    # imshow('Water Level',img)

