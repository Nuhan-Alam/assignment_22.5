from django.db import models
from django.contrib.auth.models import AbstractUser
from all.managers import CustomUserManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography= models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    membership_date = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    
    current_borrow_record = models.OneToOneField(
        'BorrowRecord', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='currently_borrowed_book'
    )
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()