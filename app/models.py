from django.db import models

# Create your models here.
class Plate(models.Model):
	CHOICES = [
        ('plate recognition', 'plate extraction'),
        ('text_extraction', 'text extraction'),   ]
	purpose = models.CharField(choices=CHOICES,default='plate recognition',max_length=50,null=True,blank=True)
	plate_img = models.ImageField(upload_to='images/')
	def __str__(self):
		return self.purpose

class Owner(models.Model):
	aadhar_number=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	education=models.CharField(max_length=100)
	email=models.EmailField(max_length=254)
	address=models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Vehical(models.Model):
	CHOICES = [
        ("Scooty","Scooty"),
        ("Luna","Luna"), 
		("Bike","Bike"),
		("Auto Riksha","Auto Riksha"),
		("Car","Car"),
		("Bus","Bus"),
		("Truck","Truck"),
		("Tempo","Tempo"),
		("Traveller","Traveller"),
		("Lorry","Lorry"),
		("Tractor","Tractor") ,
		("Heavy Vehicle","Heavy Vehicle"),]
	plate_number=models.CharField(max_length=100, primary_key=True)
	type=models.CharField(choices=CHOICES,max_length=100)
	model=models.CharField(max_length=100)
	color=models.CharField(max_length=100)
	date_of_registration=models.DateField()
	owner=models.ForeignKey('Owner',on_delete=models.CASCADE)

class Complain(models.Model):
	CHOICES = [
        ("Extreme","Extreme"),
        ("moderate","moderate"), 
		("normal","normal"),]
	severity=models.CharField(choices=CHOICES,max_length=100)
	date_of_incident=models.DateField()
	details=models.CharField(max_length=500)
	vehical=models.ForeignKey('Vehical',on_delete=models.CASCADE)

	def __str__(self):
		return self.severity

class Fine(models.Model):
	CHOICES = [
        (100,"100"),
        (500,"500"), 
		(1000,"1000"),
		(2000,"2000"),
		(5000,"5000"),]
	img = models.ImageField(upload_to='fineimg/')
	date=models.DateField()
	reason=models.CharField(max_length=800,default="parking duty")
	amount=models.IntegerField(choices=CHOICES)
	details=models.CharField(max_length=800)
	vehical=models.ForeignKey('Vehical',on_delete=models.CASCADE)

	def __str__(self):
		return self.reason