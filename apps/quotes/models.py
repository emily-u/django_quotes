from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        name = post['name']
        alias = post['alias']
        email = post['email'].lower()
        password = post['password']
        cpassword = post['cpassword']
        bday = post['bday']

        errors=[]

        if len(name)<1 or len(alias)<1 or len(email)<1 or len(password)<1 or len(cpassword)<1 or len(bday)<1 :
            errors.append("all fields are required")
        else:
            if not EMAIL_REGEX.match(email):
                errors.append("invalid email")
            else:
                if len(User.objects.filter(email=email)) > 0 :
                    errors.append('email is already used')

            if not name.isalpha() or not alias.isalpha():
                errors.append("name and alias: characters only")

            if len(password) < 3 :
                errors.append('password: at least 8 characters')
            elif password != cpassword:
                errors.append('password is not match with comfirm password, please try again')

            if len(bday) < 1 :
                errors.append("Starting date filed can not be empty!")
            else:
                date_object = datetime.strptime(bday, '%Y-%m-%d')
                if date_object < datetime.now():
                    errors.append("Starting date should not be future date!")
            
        if not errors:
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=name,
                alias=alias,
                email=email,
                password=hashed
            )
            return new_user                

        return errors

    def login_validator(self, post):
        email = post['email'].lower()
        password = post['password']

        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploader = models.ForeignKey(User, related_name="uploaded_quotes")
    liked_by = models.ManyToManyField(User, related_name="favorite")