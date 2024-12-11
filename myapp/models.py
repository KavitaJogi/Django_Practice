from django.db import models

# Create your models here.
class signmodel(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=12)
    email=models.EmailField()
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    mobile=models.BigIntegerField()

class mynotes(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=100)
    cate=models.CharField(max_length=100)
    myfile=models.FileField(upload_to='MyNotes')
    desc=models.TextField()

class contactus(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    msg=models.TextField()