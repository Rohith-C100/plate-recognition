import requests
from pprint import pprint
from django.core.mail import send_mail
from django.conf import settings
# from PIL import Image
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views import generic
from app.forms import *
from app.models import *
from json import dumps
# from django.conf import settings
# Create your views here.
# import cv2
# from matplotlib import pyplot as plt
# import numpy as np
# import imutils
# import easyocr
import json
import pytesseract
from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"

import cv2
import imutils
import numpy as np


def identify(request,pk):
    sample=Plate.objects.get(id=pk)
    if(sample.purpose=="plate recognition"):
        img = cv2.imread(sample.plate_img.path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600,400) )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray, 13, 15, 15) 

        edged = cv2.Canny(gray, 30, 200) 
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in contours:
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            print ("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        text = pytesseract.image_to_string(Cropped, lang ='eng',
        config ='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        print("Detected license plate Number is:",text)
        cv2.imwrite(sample.plate_img.path,Cropped)
        return JsonResponse(response.json(),safe=False)