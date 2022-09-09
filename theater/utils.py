from backports.zoneinfo import ZoneInfo
from django.utils import timezone
from datetime import datetime
class Utils:


    @staticmethod
    def getCurrentTime():  
        return timezone.localtime().strftime("%H:%M:00")

    @staticmethod
    def getCurrentDate():
        return timezone.localtime().strftime("%Y:%m:%d")


    