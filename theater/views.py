import http
from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Function, User,Person,Ticket,Board,Premiere
from django.views.generic import View,ListView
from django.urls import reverse
from .utils import Utils
from datetime import time,date

from pprint import pprint
# Create your views here.





class HomeView(View):
    template_name = "theater/home.html"

    def get(self,request):
        result  = Board.getAllBoard()
        return render(request,self.template_name,{"data":result})

    



class LoginView(View):
    template_name = "theater/auth/login.html"

    
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
    template_name = "theater/auth/register.html"
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


class PricesView(View):
    template_name = "theater/prices.html"

    def get(self,request):
        tickets_price = Ticket.objects.all()
        return render(request,self.template_name,{"data":tickets_price})


class BoardView(View):
    template_name = "theater/board.html"

    def get(self,request):
        result  = Board.getAllBoard()
        return render(request,self.template_name,{"data":result})

class FunctionsView(View):
    template_name = "theater/functions.html"

    def get(self,request):
        current_date = Utils.getCurrentDate()
        current_time = Utils.getCurrentTime()
        result = Function.getFunctions(current_date,current_time) 
        return render(request,self.template_name,{"data":result})


class PremiereView(View):

    template_name = "theater/premiere.html"

    def get(self,request):
        current_date = Utils.getCurrentDate()
        result = Premiere.getPremieres(current_date)
        return render(request,self.template_name,{"data":result}) 