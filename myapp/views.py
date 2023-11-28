from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Product,Category,Blog,Cart,Wishlist,Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
import requests
import razorpay

# Create your views here.

# def index(request):
# 	return HttpResponse('<h1>Hello Friends</h1>')

def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		wishlist=Wishlist.objects.filter(user=user)
		request.session['wishlist_count']=len(wishlist)
		cart=Cart.objects.filter(user=user)
		request.session['cart_count']=len(cart)
		return render(request,'index.html')
	except:
		return render(request,'index.html')

def farmer_index(request):
	return render(request,'farmer_index.html')

def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			print(">>>>>>>>>>>>>>>USER OBJECT : ",user)
			msg="Email Already Exist !!!!"
			return render(request,'signup.html',{'emsg':msg})
		except:
			user=User.objects.create(
				name=request.POST['name'],
				usertype=request.POST['usertype'],
				email=request.POST['email'],
				pswd=request.POST['pswd'],
				age=request.POST['age'],
				contact=request.POST['contact'],
				address=request.POST['address']
				)
			msg="User Registration Done..........."
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",msg)
			otp=random.randint(1000,9999)

			url = "https://www.fast2sms.com/dev/bulkV2"

			querystring = {"authorization":"NVRk2utaImAEYPfci1W6KGZO9QXhel5vUjn7wDLd0s8xro3pBCZ1A2yptsi0uxNFqQVlXKmPEYJLhS5D","variables_values":otp,"route":"otp","numbers":user.contact}

			headers = {
    			'cache-control': "no-cache"
			}

			response = requests.request("GET", url, headers=headers, params=querystring)

			print(response.text)

			return render(request,'login.html',{'any':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],pswd=request.POST['pswd'])

			request.session['email']=user.email
			request.session['name']=user.name
			print(">>>>>>>>>>>>>>>>>>>>>>>>>EMAIL SESSION : ",request.session['email'])
			if user.usertype=="farmer":
				return render(request,'farmer_index.html')
			else:
				wishlist=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlist)
				cart=Cart.objects.filter(user=user)
				request.session['cart_count']=len(cart)
				return render(request,'index.html')
		except:
			emsg="Email or Password Doesn't Matched !!!"
			return render(request,'login.html',{'emsg':emsg})
	else:
		return render(request,'login.html')

def logout(request):
	del request.session['email']
	del request.session['name']
	try:
		del request.session['image']
		del request.session['wishlist_count']
		del request.session['cart_count']
	except:
		pass
	print(">>>>>>>>>>>>>>>>>>>>>LOGOUT")
	return redirect('login')

def fpswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP for Forgot Password'
			otp=random.randint(1000,9999)
			message = f'Hi {user.name}, Your OTP is : {otp}'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )

			return render(request,'verify_otp.html',{'otp':str(otp),'email':user.email})
		except:
			emsg="No Such User Exist !!!"
			return render(request,'fpswd.html',{'emsg':emsg})
	else:
		return render(request,'fpswd.html')

def verify_otp(request):
	if request.method=="POST":
		otp=request.POST['otp']
		uotp=request.POST['uotp']
		email=request.POST['email']

		print(otp)
		print(type(otp))
		print(uotp)
		print(type(uotp))


		if otp==uotp:
			return render(request,'create_new_pswd.html',{'email':email})
		else:
			msg="OTP Doesn't Matched!!!!!"
			return render(request,'verify_otp.html',{'emsg':msg})
	else:
		msg="Something went wrong please try again later"
		return render(request,'verify_otp.html',{'emsg':msg})

def create_new_pswd(request):
	if request.method=="POST":
		email=request.POST['email']
		npswd=request.POST['npswd']
		cnpswd=request.POST['cnpswd']

		if npswd==cnpswd:
			user=User.objects.get(email=email)
			user.pswd=npswd
			user.save()
			return render(request,'login.html')
		else:
			msg="Nwe Password and Confiorm New password Doesn't Matched!!!"
			return render(request,'create_new_pswd.html',{'emsg':msg})
	else:
		msg="Something went wrong please try again later"
		return render(request,'create_new_pswd.html',{'emsg':msg})


def add_product(request):
	category=Category.objects.all()

	if request.method=="POST":
		cat=Category.objects.get(category=request.POST['cat1'])

		farmer=User.objects.get(email=request.session['email'])
		Product.objects.create(
			farmer=farmer,
			category=cat,
			pname=request.POST['pname'],
			price=request.POST['price'],
			p_img=request.FILES['p_image'],
			p_stock=request.POST['qty'],
			description=request.POST['description']
			)
		msg="Product Added......"
		return render(request,'add_product.html',{'any':msg, 'cat':category})
		
	else:
		return render(request,'add_product.html',{'cat':category})

def products(request):
	cat=Category.objects.all()
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>cats : ",cat)
	farmer=User.objects.get(email=request.session['email'])
	print("Using GET Method : ",farmer)
	product=Product.objects.filter(farmer=farmer)
	print("Using Filter Method : ",product)
	return render(request,'products.html',{'product':product,'cat':cat})

def product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'product_details.html',{'product':product})

def update_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		farmer=User.objects.get(email=request.session['email'])
		
		product.farmer=farmer
		product.pname=request.POST['pname']
		product.price=request.POST['price']
		product.p_img=request.FILES['p_image']
		product.p_stock=request.POST['qty']
		product.description=request.POST['description']
		product.save()

		return redirect('products')
	else:
		return render(request,'update_product.html',{'product':product})

def remove_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('products')

def filter(request,pk):
	cats=Category.objects.all()
	cat=Category.objects.get(pk=pk)
	prods=Product.objects.filter(category=cat)
	return render(request,"products.html",{'product':prods,'cat':cats})

def create_blog(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Blog.objects.create(
			user=user,
			title=request.POST['title'],
			image=request.FILES['image'],
			desc=request.POST['desc']
			)
		return render(request,'create_blog.html')
	else:
		return render(request,'create_blog.html')

def my_blog(request):
	farmer=User.objects.get(email=request.session['email'])
	blogs=Blog.objects.filter(user=farmer)
	return render(request,'read_blog.html',{'blogs':blogs})

def all_products_customer(request):
	prods=Product.objects.all()
	return render(request,'all_products_customer.html',{'prods':prods})


def product_detail_customer(request,pk):
	prod=Product.objects.get(pk=pk)
	return render(request,'product_detail_customer.html',{'prod':prod})

def add_to_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk)
	try:
		Wishlist.objects.get(user=user,product=prod)
		return redirect('all_products_customer')
	except:
		Wishlist.objects.create(user=user,product=prod)
		return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlist)
	return render(request,'wishlist.html',{'wishlist':wishlist})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,pk=pk)
	print(">>>>>>>>>>>>>>>>>>>>>product to be remove ",wishlist)
	wishlist.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	prod=Product.objects.get(pk=pk)
	try:
		Cart.objects.get(user=user,product=prod)
		return redirect('all_products_customer')
	except:
		Cart.objects.create(
			user=user,
			product=prod,
			qty=1,
			availability=True,
			total=prod.price,
			)
		request.session['cart_flag']=True
		return redirect('cart')

def cart(request):
	request.session['cart_flag']=True
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=False)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>CART : ")
	print(cart)
	net_price=0
	for i in cart:
		net_price+=i.total
	request.session['cart_count']=len(cart)
	try:
		
		client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
		payment = client.order.create({ "amount": net_price*100, "currency": "INR", "receipt": "order_rcptid_11" })

		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print(payment)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print(type(payment['id']))
		print(payment['id'])
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

		global payment_id
		payment_id=payment['id'] 

		cart.razorpay_order_id=payment['id']
		cart.save()
		for i in cart:
			i.save()

		return render(request,'cart.html',{'cart':cart,'net_price':net_price,'payment':payment,'total':net_price*100})
	except:
		return render(request,'cart.html',{'cart':cart,'net_price':net_price})

prod=[]
qty=[]
def success(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=False)
	net_price=0
	for i in cart:
		net_price+=i.total
		i.payment_status=True
		prod.append(i.product)
		qty.append(i.qty)
		i.save()
		i.delete()

	print(">>>>>>>>>>>product list : ",prod)
	print(">>>>>>>>>>>>>>qty list : ",qty)
	transaction = Transaction.objects.create(
		user=user,
		grand_amount=net_price,
		prod=prod,
		qty=qty,
		trans_id=payment_id,
		)

	return render(request,'success.html')

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	print(">>>>>>>>>>>>>>>>>>>>>product to be remove ",cart)
	cart.delete()
	request.session['cart_flag']=False
	return redirect('cart')

def change_qty(request,pk):
	prod=Product.objects.get(pk=pk)
	cart=Cart.objects.get(product=prod)
	cart.qty=request.POST['qty']
	cart.total=(prod.price)*int(cart.qty)
	cart.save()
	return redirect('cart')

def customer_show_blog(request):
	blog=Blog.objects.all()
	return render(request,'customer_show_blog.html',{'blog':blog})

def read_blog_unique(request,pk):
	blog=Blog.objects.get(pk=pk)
	return render(request,'read_blog_unique.html',{'blog':blog})

#========================customer Dashborad start====================================================
def c_dashboard(request):
	user=User.objects.get(email=request.session['email'])
	return render(request,'c_dashboard.html',{'user':user}) 

def c_dash_header(request):
	user=User.objects.get(email=request.session['email'])
	return render(request,'c_dash_header.html',{'user':user}) 


def c_dash_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.name=request.POST['uname']
		try:
			user.image=request.FILES['image']
		except:
			pass
		user.usertype=request.POST['utype']
		user.email=request.POST['uemail']
		user.pswd=request.POST['upswd']
		user.age=request.POST['uage']
		user.contact=request.POST['ucontact']
		user.address=request.POST['uaddress']
		user.save()
		return redirect('c_dash_header')
	else:
		return render(request,'c_dash_profile.html',{'user':user})

def d_cart(request):
	request.session['cart_flag']=True
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=False)
	print(">>>>>>>>>>>>>>>>>>CART in dash")
	print(cart)
	return render(request,'d_cart.html',{'cart':cart,'user':user})

def rd_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	print(">>>>>>>>>>>>>>>>>>>>>product to be remove ",cart)
	cart.delete()
	request.session['cart_flag']=False
	return redirect('d_cart')

def order_history(request):
	user=User.objects.get(email=request.session['email'])
	transaction=Transaction.objects.filter(user=user)
	return render(request,'order_history.html',{'user':user,'trans':transaction})

#=========================customer Dashboard End===================================== 


# ORM : Object Relational Mapping 
# to convert object to relational(tabular format) and reconvert relation to object format

# .create() : use to insert data to table
# syntax : model_name.objects.create()  

# .get() : to fetch data from data table : It will return single object 
# syntax : model_name.objects.get(condition)


# .filter() : to fetch one or more data as per condition : It will return QuerySet
# Syntax : model_name.objects.filter(condition)  

# .all() : to fetch all the records from the table
# Syntax : model_name.objects.all()