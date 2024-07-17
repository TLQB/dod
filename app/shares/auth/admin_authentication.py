from rest_framework import authentication 
from django.http.request import HttpRequest 

def authenticate(self, request: HttpRequest, name: str, password: str):
	admin = Admin.objects.filter(name=name, password= password).first()

	if admin is None:
		raise 