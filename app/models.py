from django.db import models

# Create your models here.
class Plate(models.Model):
	CHOICES = [
        ('plate recognition', 'plate extraction'),
        ('text_extraction', 'text extraction'),   ]
	purpose = models.CharField(choices=CHOICES,default='plate recognition',max_length=50,null=True,blank=True)
	plate_img = models.ImageField(upload_to='images/')
