from __future__ import unicode_literals
import bcrypt, re
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.
class UserManager(models.Manager):
    def login(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['password']) == 0:
                errors['password'] = "Please Enter a Password"
            if len(kwargs['email']) == 0:
                errors['email'] = "Please Enter an Email"
            if len(errors) != 0:
                return (False, errors)
            else:
                user = User.userMgr.filter(email=kwargs['email'])
                if not user:
                    errors['user'] = "Email/Password Combination Not Found"
                    return (False, errors)
                else:
                    if bcrypt.checkpw(kwargs['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                        return (True, user[0])
                    else:
                        errors['user'] = "Email/Password Combination Not Found"
                        return (False, errors)

    def register(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['name']) < 2:
                errors['name'] = "Name must be at least 2 characters"
            if len(kwargs['alias']) < 2:
                errors['alias'] = "Alias must be at least 2 characters"
            if len(kwargs['email']) == 0:
                errors['email'] = "Email is required"
            elif not EMAIL_REGEX.match(kwargs['email']):
                errors['email'] = "Please enter a valid email"
            if len(kwargs['password']) < 8:
                errors['password'] = "Password must be at least 8 characters"
            if kwargs['password'] != kwargs['c_password']:
                errors['c_password'] = "Passwords must match"
            if len(errors) is not 0:
                return (False, errors)
            else:
                hashed = bcrypt.hashpw(kwargs['password'].encode('utf-8'), bcrypt.gensalt())
                user = User.userMgr.create(name=kwargs['name'], alias=kwargs['alias'], email=kwargs['email'], password=hashed)
                user.save()
                return (True, user)
        else:
            messages.add_message(request, messages.INFO, "Please Try Registration Again")
            return

class User(models.Model):
    name        = models.CharField(max_length=45)
    alias       = models.CharField(max_length=45)
    email       = models.EmailField(max_length=100)
    password    = models.CharField(max_length=100)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)
    userMgr     = UserManager()

class BookManager(models.Manager):
    def add(self, **kwargs):
        errors = {}
        if len(kwargs['title']) < 4:
            errors['title'] = "Title Must Have at Least 4 Characters"
        if len(kwargs['author']) < 5:
            errors['author'] = "Author Must Have at Least 5 Characters"
        if len(kwargs['review']) < 10:
            errors['review'] = "Review Must Have at Least 10 Characters"
        if kwargs['rating'] < 1 or kwargs['rating'] > 5:
            errors['rating'] = "That Rating Is Not Allowed"
        if kwargs['user'] is None:
            errors['user'] = "No User Found, Please Log Out and Log Back In"
        if len(errors) is not 0:
            return (False, errors)
        else:
            b = Book.bookMgr.create(
                title  = kwargs['title'],
                author = kwargs['author'],
            )
            u = User.userMgr.get(id=kwargs['user'])
            rev = Review.objects.create(
                user    = u,
                book    = b,
                review  = kwargs['review'],
                rating  = kwargs['rating']
            )
            return (True, b)

    def add_review(self, **kwargs):
        print "===add_review==="
        errors = {}
        if len(kwargs['review']) < 10:
            errors['review'] = "Review Must Have at Least 10 Characters"
        if kwargs['rating'] < 1 or kwargs['rating'] > 5:
            errors['rating'] = "That Rating Is Not Allowed"
        if kwargs['user'] is None:
            errors['user'] = "No User Found, Please Log Out and Log Back In"
        if kwargs['book'] is None:
            errors['book'] = "No Book Found, Please Try Again"
        if len(errors) is not 0:
            return (False, errors)
        else:
            u = User.userMgr.get(id=kwargs['user'])
            b = Book.bookMgr.get(id=kwargs['book'])
            r = Review.objects.create(
                user   = u,
                book   = b,
                review = kwargs['review'],
                rating = kwargs['rating']
            )
            return (True, int(kwargs['book']))

class Book(models.Model):
    title       = models.CharField(max_length=100)
    author      = models.CharField(max_length=100)
    reviewers   = models.ManyToManyField(User, through='Review')
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)
    bookMgr     = BookManager()
    def __unicode__(self):
        return "%s %s" % (self.title, self.author)

class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    review      = models.TextField()
    rating      = models.IntegerField()
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)
