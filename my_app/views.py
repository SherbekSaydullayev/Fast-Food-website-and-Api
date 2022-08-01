from django.shortcuts import render
from django.views.generic import TemplateView,ListView,CreateView
from .models import Product,Comment,Order
from django.core.paginator import Paginator
import requests
from django.urls import reverse_lazy






class HomePageView(TemplateView):
	template_name = 'home.html'

class IndexPageView(ListView):
	model = Product
	template_name = 'index.html'

# class MenuPageView(ListView):
# 	model = Product
# 	template_name = 'menu.html'
# 	context_object_name = 'maxsulotlar'


def MenuPageView(request):
	if request.user.is_authenticated:
		customer = request.user
		print(request.user)
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items # Savatdagi mahsulot nomi
	else:
		items = []
		order = {'get_cart_total': 0, "get_cart_items": 0}
		cartItems = order['get_cart_items']

	obj = Product.objects.all()
	page_n = request.GET.get('page',1)
	p = Paginator(obj,2)
	try:
		page = p.page(page_n)
	except Exception:
		page = p.page(1)
	context = {
	'page':page,
	'cartItems':cartItems
	}
	return render(request,'menu.html',context)

class AboutPageView(ListView):
	model = Product
	template_name = 'about.html'

class ProductCreateView(CreateView):
	model = Product
	template_name = 'product_create.html'
	# fields = ('mahsulot_nomi','mahsulot_tarkibi','mahsulot_rasmi','mahsulot_narxi')
	fields = '__all__'
	success_url = reverse_lazy('index')



def telegram_bot_sendtext(bot_message):
	bot_token = '5184089123:AAEH5YHYE3J0FHya9qTq8WNDUjOR2w8ETVk'
	bot_chatID = '1168299390'
	send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+bot_message
	response = requests.get(send_text)
	return response.json()
# class BookPageView(ListView):
# 	model = Product
# 	template_name = 'book.html'

def BookPageView(request):
	if request.method == 'POST':
		name = request.POST.get('name',None)
		phone = request.POST.get('phone',None)
		email = request.POST.get('email',None)
		message = request.POST.get('message',None)
		user = Comment.objects.create(
			userName = name,
			phone = phone,
			email = email,
			message = message
			)
		user.save()

		telegram_bot_sendtext(f"Ismi:{user}\nEmail:{email}\nTel:{phone}\nXabar:{message}")

	return render(
	request = request,
	template_name = 'book.html'
		)



