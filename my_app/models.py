from django.db import models
from accounts.models import User

class Product(models.Model):
	name = models.CharField(max_length = 500)
	description = models.TextField()
	price = models.CharField(max_length = 100)
	image = models.ImageField(upload_to = 'image/')

	def __str__(self):
		return self.name


class Comment(models.Model):
	userName = models.CharField(max_length = 300, null = True)
	phone = models.CharField(max_length = 20)
	email = models.CharField(max_length = 50)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		return f'{self.userName}'


# 1-bosqich
# Order yani mahsulotni savatga qushish uchun model
# from django.contrib.auth.models import User

class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	date_orderd = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200,null=True)
	complete =  models.BooleanField(default=False,null=True,blank=False)

	# pastdagi get_total funksiyasidan qaytagan qiymatni barcha
	# OrderItem(savatdagi mahsulotlar) larni hisoblash uchun

	@property # Dekorator
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	# String obyektini qaytaradi	
	def __str__(self):
		return str(self.id)
# Mahsulotni qachon va kim totmonidan qaysi mahsulot qushilganligini saqlash uchun model
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
	quantity = models.IntegerField(default=0,null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)



	# Mahsulot soniga qarab Kopaytirib beradi
	@property #Dekorator
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	# String obyektini qaytaradi
	def __str__(self):
		return str(self.id)

# 2-bosqich
# ===> base.html ga 