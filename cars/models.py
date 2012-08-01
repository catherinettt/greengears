from django.db import models

from djangoratings.fields import RatingField
from django.contrib.auth.models import User


class Year(models.Model):
    YEAR = models.IntegerField()
    def __unicode__(self):
        #return self.YEAR
        return u"%d"% (self.YEAR)

class Make(models.Model):
    MAKE_NAME = models.CharField(max_length=25)
    def __unicode__(self):
        return self.MAKE_NAME

class Model(models.Model):
    MODEL_NAME = models.CharField(max_length=30)
    MAKE_ID = models.ForeignKey(Make)
    def __unicode__(self):
        return self.MODEL_NAME

class Car(models.Model):
    YEAR = models.ForeignKey(Year)
    MAKE = models.ForeignKey(Make)
    MODEL = models.ForeignKey(Model)
    MPG = models.FloatField()
    HP = models.IntegerField()
    BODYTYPE = models.CharField(max_length=20)
    TRANSMISSION = models.CharField(max_length=20)
    NUM_GEARS = models.IntegerField()
    DRIVETRAIN = models.CharField(max_length=20)
    SIL = models.CharField(max_length=20)
    AXELRATIO = models.FloatField()
    NVRATIO = models.FloatField()
    CURBWEIGHT = models.IntegerField()
    CO2 = models.FloatField()
    CO = models.FloatField()
    THC = models.FloatField()
    NOX = models.FloatField()
    AFTERTREATMENT_DEVICE = models.CharField(max_length=50)
    CYLINDER = models.IntegerField()
    #image count variable for each car, used to create unique and dynamic image names for uploads
    COUNT = models.IntegerField(default=0) 
    RATING = RatingField(range=5, allow_anonymous=True, can_change_vote=True, use_cookies=False)
    def __unicode__(self):
        return u"%s %s"% (self.MAKE, self.MODEL)

class Comment(models.Model):
    CAR = models.ForeignKey(Car)
    COMMENT = models.CharField(blank=True, max_length=255)
    NAME = models.CharField(max_length=20)
    DATE = models.DateTimeField()
    def __unicode__(self):
        return self.COMMENT


class Images(models.Model):
    CAR = models.ForeignKey(Car)
    IMAGE = models.ImageField(upload_to = 'car_img', blank=True, help_text='Upload an image')
    #IMAGE = models.ImageField(storage = FS, blank = True, help_text='Upload an image')
    def __unicode___(Images):
        return self.IMAGE

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    accepted_eula = models.BooleanField()
    favorite_animal = models.CharField(max_length=20, default="Dragons.")
