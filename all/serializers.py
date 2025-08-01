from rest_framework import serializers
from all.models import Book,User,Category,Author,BorrowRecord

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description','book_count']

    book_count = serializers.IntegerField(read_only=True)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography','book_count']
    book_count = serializers.IntegerField(read_only=True)