from django.db import models
import re
from datetime import datetime, date
from django.db.models.fields import CharField 

def calculate_age(born):
    today = date.today()
    born = datetime.strptime(born,'%Y-%m-%d').date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class UserManager(models.Manager):
            
    def validations_signup(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        LETTERS = re.compile(r'[a-zA-Z]+$')
        LETTERS_NUMBERS = re.compile(r'[a-zA-Z0-9]+$')

        errors = {}
        if len(postData['first_name'])<2:    
            errors['fname_length'] = "First name is too short. Re entry!"
        if len(postData['last_name'])<2:
            errors['lname_length'] = "Last name is too short. Retry!"
        if (not LETTERS.match(postData['first_name'])) or (not LETTERS.match(postData['last_name'])):
            errors["name"] = "Invalid name characters. Re entry!"
        if (not EMAIL_REGEX.match(postData["email"])):
            errors['email'] = "Invalid email format. Retry!"
        if(len(postData['pwd']))<8:
            errors['password'] = "Password format must have at least 8 characters. Re entry!"
        if(postData['pwd'] != postData['check_pwd']):
            errors['password_validate'] = "Passwords must be equal. Re entry!"
        if postData['bday'] > datetime.now().strftime('%Y-%m-%d'):
            errors['bday'] = "Check your Birthday Date, it can't be a date in future. Re entry!"        
        if calculate_age(postData['bday'])<13:
            errors['year'] = "To register you must have more than 13 years old."
        return errors

    def validations_login(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        LETTERS = re.compile(r'[a-zA-Z]+$')
        LETTERS_NUMBERS = re.compile(r'[a-zA-Z0-9]+$')

        errors = {}
        if not EMAIL_REGEX.match(postData["email"]):
            errors['email'] = "Invalid email format. Retry!"
        if(len(postData['pwd']))<8:
            errors['password'] = "Password format must have at least 8 characters. Re entry!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=70)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() #Validate data

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
