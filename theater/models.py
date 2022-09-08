from django.db import models

# Create your models here.


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    legal_document = models.CharField(max_length=32,unique=True)
    email = models.CharField(max_length=128)
    gender = models.CharField(max_length=16)
    phone = models.CharField(max_length=32)
    state = models.CharField(max_length=16)
    country = models.CharField(max_length=16)
    address = models.CharField(max_length=128)
    birth_date = models.DateField()


    def __str__(self):
        return f"{self.name} {self.last_name}"


    @classmethod
    def checkIfPersonExists(self,legal_document):
        try:
            person = Person.objects.get(legal_document=legal_document)
            return {"person":person,"state":True}
        except Person.DoesNotExist:
            return {"person":None,"state":False}

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person,on_delete=models.DO_NOTHING)
    username = models.CharField(max_length=64,unique=True)
    password = models.CharField(max_length=64)


    def __str__(self):
        return f"{self.username}"
    @classmethod
    def CheckIfUserExists(self,username):
        try:
            user = User.objects.get(username=username)
            return {"user":user,"state":True}
        except:
            return {"user":None,"state":False}

    

class Movie(models.Model): 
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    genre = models.CharField(max_length=32)
    duration = models.TimeField()
    banner_url = models.CharField(max_length=256)
    release_date = models.DateField()
    rating = models.CharField(max_length=8)
    language = models.CharField(max_length=32)
    subtitle = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.title} - {self.release_date}"

class Function(models.Model):
    function_id = models.AutoField(primary_key=True)
    time  = models.TimeField()
    date = models.DateField()
    seat_amount = models.IntegerField()
    room = models.CharField(max_length=32)
    movie =  models.ForeignKey(Movie,on_delete=models.DO_NOTHING)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32)
    price = models.FloatField()
    format = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.type} - {self.price}"



