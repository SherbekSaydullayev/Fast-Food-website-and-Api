from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from my_app.models import Product
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate



class AuthUserRegistrationView(APIView):
	def post(self, request, *args, **kwargs):
		serializer = UserSerializers(data=request.data)
		for user in User.objects.all():
			if not user:
				break
			else:
				try:
					Token.objects.get(user_id=user.id)
				except Token.DoesNotExist:
					Token.objects.create(user=user)
		if serializer.is_valid():
			user = serializer.save()
			token = Token.objects.create(user=user)
			return Response(
				{
					"user":{
						"id":serializer.data["id"],

						"username":serializer.data["username"],
					},
					"status":{
						"message":"User created",
						"code":f"{status.HTTP_200_OK} OK",
					},
					"token": token.key,
				}
			)
		return Response(
			{
				"error": serializer.errors,
				"status": f"{status.HTTP_203_NON_AUTHORITATIVE_INFORMATION}\
					NON_AUTHORITATIVE_INFORMATION",
			}
		)



class ProductSerializersView(ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializers



class ProductIDSerializersView(RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Product.objects.all()
	serializer_class = ProductSerializers




def register_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username=username,password=password)
		user.save()
		return redirect('login')

	ctx = {}
	return render(request,'signup.html',ctx)




def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username= username,password=password)
		if user:
			login(request,user)
			return redirect('index')

		# user = User.objects.create_user(username=username,password=password)
		# user.save()
		# return redirect('index')

	ctx = {}
	return render(request,'registration/login.html',ctx)


def logout_user(request):
	logout(request)
	return redirect('index')



# class UserCreateView(generic.CreateView):
# 	form_class = UserCreationForm
# 	template_name = 'signup.html'
# 	success_url = reverse_lazy('login')
