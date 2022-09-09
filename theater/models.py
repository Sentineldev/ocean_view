from threading import local
from django.db import models
from pprint import pprint
import locale


locale.setlocale(locale.LC_TIME,'es_VE.utf8')

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

    @staticmethod
    def getDictMovie(object):
        return {
            "movie_id":object.movie_id,
            "title":object.title,
            "description":object.description,
            "genre":object.genre,
            "duration":object.duration.strftime("%H:%M"),
            "banner_url":object.banner_url,
            "release_date":object.release_date.strftime("%Y:%m:%d"),
            "rating":object.rating,
            "language":object.language,
            "subtitle":object.subtitle
        }

class Function(models.Model):
    function_id = models.AutoField(primary_key=True)
    time  = models.TimeField()
    date = models.DateField()
    seat_amount = models.IntegerField()
    room = models.CharField(max_length=32)
    movie =  models.ForeignKey(Movie,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.movie.title} {self.room}"



    
    


    @staticmethod
    def getDictFunction(object):
        return {
            "function_id":object.function_id,
            "time":object.time.strftime("%H:%M %p"),
            "date":object.date.strftime("%Y:%m:%d"),
            "seat_amount":object.seat_amount,
            "movie_id":object.movie_id,
            "room":object.room
        }


    @staticmethod
    def __OrderMoviesAndFunctions(Functions):
        returned_dict = {}
        for f in Functions:
            if not f.title in returned_dict:
                returned_dict[f.title] = {"movie":Movie.getDictMovie(f),"functions":[Function.getDictFunction(f)]}
            else:
                returned_dict[f.title]['functions'].append(Function.getDictFunction(f))
        return returned_dict

    @staticmethod
    def getFunctions(current_date,current_time):
        result = Function.objects.raw(
            '''
            SELECT * FROM theater_function as `tf`
            JOIN theater_movie as `tm` ON tm.movie_id = tf.movie_id
            WHERE tf.date >= %s AND tf.time >= %s ORDER BY tf.movie_id,time
            ''',[current_date,current_time]
        )

        return Function.__OrderMoviesAndFunctions(result)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32)
    price = models.FloatField()
    format = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.type} - {self.price}"



class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    movie =  models.ForeignKey(Movie,on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"{self.movie_id}"
    @staticmethod
    def getAllBoard():
        return Board.objects.raw(
            """
            SELECT * FROM theater_board as `tb`
            JOIN theater_movie as `tm` ON tb.movie_id = tm.movie_id
            """
        )


class Premiere(models.Model):

    premiere_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie,on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"

    @staticmethod
    def getPremiereDict(object):

        return {
            "premiere_id":object.premiere_id,
            "movie_id":object.movie_id,
            "date":object.date.strftime("%B %d %A"),
            "optional_date":object.date.strftime("%A %d")
        }


    @staticmethod 
    def OrderPremieres(Premieres):
        returned_dict = {}
        for premiere in Premieres:
            dict = Premiere.getPremiereDict(premiere)
            movie = Movie.getDictMovie(premiere)
            month = dict["date"].split(" ")[0] 

            
            if not month in returned_dict:
                returned_dict[month] = {"premieres":[{"movie":movie,"premiere":dict}]}
            else:
                returned_dict[month]['premieres'].append({"movie":movie,"premiere":dict})
        return returned_dict

    @staticmethod
    def getPremieres(current_date):
        query = Premiere.objects.raw(
            """
            SELECT * FROM theater_premiere as `tp`
            JOIN theater_movie as `tm` ON tm.movie_id = tp.movie_id
            WHERE tp.date >= %s ORDER BY tp.date
            """,[current_date]
        )         
        return Premiere.OrderPremieres(query)    