# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 13:50:35 2021

@author: acer
"""

# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_smile.xml
import cv2
import matplotlib.pylab as plt
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Face Detection Viola-Jones/Haar Like (333210037)')

width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))

face_cascade = cv2.CascadeClassifier('models/face_detect/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('models/face_detect/haarcascade_eye.xml') # haarcascade_eye_tree_eyeglasses.xml
smile_cascade = cv2.CascadeClassifier('models/face_detect/haarcascade_smile.xml')

img = cv2.imread('images/all.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.01, 8) # scaleFactor=1.2, minNbr=5
print(len(faces)) # number of faces detected
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.04, 10)
    #print(eyes) # location of eyes detected
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    smile = smile_cascade.detectMultiScale(roi_gray, 1.38, 6)
    for (mx,my,mw,mh) in smile:
        cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,0,255),2)
       
plt.figure(figsize=(15,20))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.axis('off')
plt.tight_layout()
plt.show()

#program GUI
#ubah skala gambar input
photoInput = Image.open("images/all.png")
newsize = (440,568)
resize_image1 = photoInput.resize(newsize)
imgInput = ImageTk.PhotoImage(resize_image1)

#ubah skala gambar output
image_rgb = img
cv2.imwrite('images/allFace.png',image_rgb)
photoOutput = Image.open("images/allFace.png")
newsize = (440,568)
resize_image2 = photoOutput.resize(newsize)
imgOutput = ImageTk.PhotoImage(resize_image2)

labelInput = "Input Image"
labelOutput = "Output Image"

image_list = [imgInput, imgOutput]
label_list = [labelInput,labelOutput]

showLabel = Label(text = label_list[0], font = "Verdana 16 bold")
showLabel.place(x = 600, y = 10)

showImage = Label(image = image_list[0])
showImage.place(x=470, y = 50)

def forward(image_number, label_number):
    global showLabel
    global showImage    
    global button_forward
    global button_back

    showLabel.place_forget()
    showImage.place_forget()
    
    showLabel = Label(text=label_list[label_number-1], font = "Verdana 16 bold")
    showLabel.place(x = 600, y = 10)
    showImage = Label(image = image_list[image_number-1])
    showImage.place(x=470, y = 50)
    
    button_forward = Button(root, text="Forward", command=lambda: forward(image_number+1, label_number+1))
    button_back = Button(root, text="Back", command=lambda: back(image_number-1, label_number-1))

    if image_number == 2:
        button_forward = Button(root, text="Forward", state=DISABLED)
       
                        
    
    button_back.place(x=500, y = 650)
    button_forward.place(x=800, y=650)

def back(image_number, label_number):
    global showLabel
    global showImage    
    global button_forward
    global button_back
    
    showLabel.place_forget()
    showImage.place_forget()
    
    showLabel = Label(text = label_list[label_number-1], font = "Verdana 16 bold")
    showLabel.place(x = 600, y = 10)
    showImage = Label(image= image_list[image_number-1])
    showImage.place(x=470, y = 50)
    
    button_forward = Button(root, text="Forward", command=lambda: forward(image_number+1, label_number+1))
    button_back = Button(root, text="Back", command=lambda: back(image_number-1, label_number-1))

    if image_number == 1:
        button_back = Button(root, text="Back", state=DISABLED)
       
                            
    button_back.place(x=500, y = 650)
    button_forward.place(x=800, y=650)

                            
button_back = Button(root, text="Back", command=back, state=DISABLED)
button_forward = Button(root, text="Forward", command=lambda: forward(2,2))
button_back.place(x=500, y = 650)
button_forward.place(x=800, y=650)
                            

                            
root.mainloop()