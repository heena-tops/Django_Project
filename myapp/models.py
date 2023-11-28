from django.db import models
from django.utils import timezone 

# Create your models here.
class User(models.Model):
	name=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100)
	email=models.EmailField()
	pswd=models.CharField(max_length=100)
	age=models.IntegerField()
	contact=models.BigIntegerField()
	address=models.CharField(max_length=500)
	image=models.ImageField(upload_to='user/',default='user/person.png')

	def __str__(self):
		return self.name+" - "+self.usertype

class Category(models.Model):
	category=models.CharField(max_length=100)

	def __str__(self):
		return self.category


class Product(models.Model):
	farmer=models.ForeignKey(User,on_delete=models.CASCADE)
	category=models.ForeignKey(Category,on_delete=models.CASCADE)
	pname=models.CharField(max_length=100)
	price=models.IntegerField()
	p_img=models.ImageField(upload_to='images/')
	p_stock=models.IntegerField()
	description=models.CharField(max_length=500)

	def __str__(self):
		return self.pname

class Blog(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	title=models.CharField(max_length=100)
	image=models.ImageField(upload_to='blog_images/')
	desc=models.TextField()

	def __str__(self):
		return self.title+' - '+self.user.name+f'({self.user.usertype})'

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	qty=models.IntegerField()
	availability=models.BooleanField() # based on stock available from farmer 
	payment_status=models.BooleanField(default=False)
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
	total=models.IntegerField()
	date=models.DateTimeField(default=timezone.now())

	def __str__(self):
		return self.product.pname+f"{self.payment_status}"+self.user.name

class Transaction(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	grand_amount=models.IntegerField()
	trans_id=models.CharField(max_length=100,null=True,blank=True)
	prod=models.CharField(max_length=100,null=True)
	qty=models.CharField(max_length=100,null=True)
	date=models.DateField(default=timezone.now())

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.product.pname+" "+self.user.name