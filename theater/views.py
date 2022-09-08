import http
from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User,Person
from django.views.generic import View
from django.urls import reverse
# Create your views here.





class HomeView(View):
    template_name = "theater/views/home.html"

    def get(self,request):

        return render(request,self.template_name)

    



class LoginView(View):
    template_name = "theater/views/auth/login.html"

    
    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):

        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username,password=password)
            return HttpResponseRedirect(reverse('theater:home'))
        except User.DoesNotExist:
            response = {"message":"Usuario incorrecto","state":False}
        
        return render(request,self.template_name,response)


class RegisterView(View):
    template_name = "theater/views/auth/register.html"
    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        
        user = User()
        person = Person()
        user.username = request.POST['username']
        user.password = request.POST['password']
        
        person.name = request.POST['name']    
        person.last_name = request.POST['last_name']
        person.legal_document = request.POST['legal_document']
        person.email = request.POST['email']
        person.gender = request.POST['gender']
        person.phone = request.POST['phone']
        person.state = request.POST['state']
        person.country = request.POST['country']
        person.address = request.POST['address']
        person.birth_date = request.POST['birth_date']

        if not user.CheckIfUserExists(user.username)['state'] and not person.checkIfPersonExists(person.legal_document)['state']:
            try:
                person.save()
                person = Person.objects.get(legal_document=person.legal_document)
                user.person = person
                user.save()
                response = {"message":"Registrado exitosamente!","state":True}
            except Exception as e:
                print(e)
                response = {"message":"Hubo un error al registrar el usuario","state":False}            
        else:
            response = {"message":"La Cedula o el Usuario ya se encuentran registrados","state":False}

        return render(request,self.template_name,response)