from django.shortcuts import render
from all.serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet
from all.models import Category,Author
from django.db.models import Count

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = CategorySerializer


