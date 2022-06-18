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
from django.core.files.storage import default_storage,get_storage_class
import os
from django.conf import settings
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

# class NpEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.integer):
#             return int(obj)
#         if isinstance(obj, np.floating):
#             return float(obj)
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return super(NpEncoder, self).default(obj)

def identify(request,pk):
    sample=Plate.objects.get(id=pk)
    if(sample.purpose=="plate recognition"):
        regions = ['mx', 'us-ca'] # Change to your country
        with open(sample.plate_img.path, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token 8834d47427b21930011e3376c2d87c2782ddc9cc'})
        # pprint(response.json())
        pprint(response.json())
        return JsonResponse(response.json(),safe=False)
    else:
        IMAGE_PATH =sample.plate_img.path
        text=pytesseract.image_to_string(Image.open(IMAGE_PATH), lang ='eng')
        return JsonResponse(text,safe=False)

def display(request,pk):

    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            plate_number=form.cleaned_data['plate_number']
            try:
                vehical = Vehical.objects.get(pk=plate_number)
            except Vehical.DoesNotExist:
                return HttpResponseRedirect(reverse('notexist'))
            return HttpResponseRedirect(reverse('vehical',args=[plate_number]) )
    else:
        img= Plate.objects.get(id=pk)
        form=SearchForm()
        context={
                'plate' : img,
                'id':pk,
                'form':form,
                 } 
        if(img.purpose=="plate recognition"):
            return render(request, 'app/display_plate.html',context)
        else:
            return render(request, 'app/display_text.html',context)

def fine_vehicle(request,pnum):
    vehical = get_object_or_404(Vehical, pk=pnum)

    if request.method == 'POST':

        form = FineForm(request.POST, request.FILES)

        if form.is_valid():
            fine=form.save(commit=False)
            fine.vehical=vehical
            fine.save()
            subject = fine.reason
            message = fine.details+"\n"+"fine amount: "+str(fine.amount)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [vehical.owner.email,]
            send_mail( subject, message, email_from, recipient_list,fail_silently=False)
            return HttpResponseRedirect(reverse('success'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FineForm()

        context = {
            'form': form,
            'vehical': vehical,
        }

        return render(request, 'app/fine_form.html', context)

def complain_vehicle(request,pnum):
    vehical = get_object_or_404(Vehical, pk=pnum)

    if request.method == 'POST':

        form = ComplainForm(request.POST, request.FILES)

        if form.is_valid():
            complain=form.save(commit=False)
            complain.vehical=vehical
            complain.save()
            return HttpResponseRedirect(reverse('success'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = ComplainForm()

        context = {
            'form': form,
            'vehical': vehical,
        }

        return render(request, 'app/complain_form.html', context)



def success(request):
    return render(request, 'app/submitted.html')

def notexist(request):
    return render(request, 'app/notexist.html')

class VehicalDetailView(generic.DetailView):
    model = Vehical
    template_name = 'app/vehical_detail.html'
    context_object_name = 'vehical'


def search(request):
    if request.method == 'POST':

        form = SearchForm(request.POST)
        if form.is_valid():
            plate_number=form.cleaned_data['plate_number']
            try:
                vehical = Vehical.objects.get(pk=plate_number)
            except Vehical.DoesNotExist:
                vehical = None

            context = {
                'vehical': vehical,
                'form': form
            }
        return render(request, 'app/search.html', context)  
    else:
        form = SearchForm()
        vehical=None
        context = {
            'vehical': vehical,
            'form': form
        }

        return render(request, 'app/search.html', context)

def vehical_histroy(request):

    if request.method == 'POST':

        form = HistoryForm(request.POST)
        if form.is_valid():
            plate_number=form.cleaned_data['plate_number']
            type=form.cleaned_data['type']
            complain_list=None
            fine_list=None
            try:
                vehical = Vehical.objects.get(pk=plate_number)
            except Vehical.DoesNotExist:
                return HttpResponseRedirect(reverse('notexist'))
            if(type=="complain"):
                complain_list = Complain.objects.filter(vehical=vehical)
            else:
                fine_list=Fine.objects.filter(vehical=vehical)
            context = {
                'complain_list': complain_list,
                'fine_list':fine_list,
                'form': form
            }
            return render(request, 'app/vehical_history.html', context)  
    else:
        form = HistoryForm()
           
    context = {
        'form': form
    }

    return render(request, 'app/vehical_history.html', context)

class ComplainDetailView(generic.DetailView):
    model = Complain
    template_name = 'app/complain_detail.html'
    context_object_name = 'complain'

class FineDetailView(generic.DetailView):
    model = Fine
    template_name = 'app/fine_detail.html'
    context_object_name = 'fine'

def doc_search(request):

    if request.method == 'POST':

        form = SearchForm(request.POST)
        if form.is_valid():
            plate_number=form.cleaned_data['plate_number']
            try:
                vehical = Vehical.objects.get(pk=plate_number)
            except Vehical.DoesNotExist:
                vehical = None
            result=[]
            for filename in os.listdir(os.path.join(os.getcwd() ,'staticfiles/docs')):
                file1 = default_storage.open(os.path.join('docs',filename), 'r')
                string = plate_number
                index = 0
                temp={}
                # Loop through the file line by line
                index=0
                for line in file1:  
                    index += 1 
                    
                    # checking string is present in line or not
                    if string in line:
                        temp['file']=filename
                        line=line.replace(string," <mark> "+string+" </mark> ")
                        temp[index]=line
                if len(temp)!=0:
                    result.append(temp)
                # closing text file    
                file1.close() 
            context = {
                'vehical': vehical,
                'form': form,
                'result':result
            }
        return render(request, 'app/search_doc.html', context)  
    else:
        form = SearchForm()
        vehical=None
        context = {
            'vehical': vehical,
            'form': form
        }
        return render(request, 'app/search_doc.html', context)