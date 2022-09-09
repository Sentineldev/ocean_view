from django.contrib import admin

from .models import  Ticket,Board,Movie,Function,Premiere
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Board)
admin.site.register(Movie)
admin.site.register(Function)
admin.site.register(Premiere)
