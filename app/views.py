# from PIL import Image
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from app.forms import *
from app.models import *
from json import dumps
# from django.conf import settings
# Create your views here.
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import json



def index(request):
    return render(
        request,
        'app/index.html',
    )



def signup(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = sign_up_form(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user = User.objects.create_user(form.cleaned_data['first_name'],form.cleaned_data['email_id'], form.cleaned_data['password'])
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = sign_up_form()

    context = {
        'form': form,
    }

    return render(request, 'app/signup.html', context)




# Create your views here.
def image_upload_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            a=form.save()
            return HttpResponseRedirect(reverse('display',args=[a.id]) )
    else:
        form = ImageForm()
    return render(request, 'app/image_upload.html', {'form' : form})


def success(request):
	return HttpResponse('successfully uploaded')

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def identify(request,pk):
    sample=Plate.objects.get(id=pk)
    if(sample.purpose=="plate recognition"):
        img = cv2.imread(sample.plate_img.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 30, 200) #Edge detection


        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]


        location = 0
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break


        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)


        # plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]


        # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))


        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)


        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        cv2.imwrite(sample.plate_img.path, res)

        # print(result)
        # print(text)
        # print(type(result))
        # for t in result:
        #     print(t)
        jresult=dumps(result, cls=NpEncoder)
        return JsonResponse(jresult,safe=False)
    else:
        IMAGE_PATH =sample.plate_img.path
        reader = easyocr.Reader(['en'],gpu=False)
        result = reader.readtext(IMAGE_PATH,paragraph="True")
        jresult=dumps(result, cls=NpEncoder)
        return JsonResponse(jresult,safe=False)


def display(request,pk):
        img= Plate.objects.get(id=pk)
        context={
                'plate' : img,
                'id':pk,
                 } 
        if(img.purpose=="plate recognition"):
            return render(request, 'app/display_plate.html',context)
        else:
            return render(request, 'app/display_text.html',context)


    




