from rest_framework import serializers
from all.models import Book,User,Category,Author,BorrowRecord
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from all.models import Book

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


class BookReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'current_borrow_record']

class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'current_borrow_record']




class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()

class BorrowSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = BorrowRecord
        fields = ['id','book', 'member', 'borrow_date','return_date']
        read_only_fields = ['member','borrow_date','book']
    
    def get_user(self, obj):
        return SimpleUserSerializer(obj.member).data

    def create(self, validated_data):
        """
        Create borrow record
        """
        user = self.context['user']
        book_id = self.context['book_id']
        book = Book.objects.get(id=book_id)
        record = BorrowRecord.objects.create(member=user,book=book,**validated_data)
        book.current_borrow_record = record
        book.save()
        return record

    def validate(self, data):
        """
        Object-level validation with double checking
        """
        return_date = data.get('return_date')
        if return_date:
            today = timezone.now().date()
            max_return_date = today + timedelta(days=30)
            
            if return_date < today:
                raise serializers.ValidationError({
                    'return_date': 'Return date cannot be in the past.'
                })
            
            if return_date > max_return_date:
                raise serializers.ValidationError({
                    'return_date': 'You cannot borrow for more than 30 days.'
                })
        
        book_id = self.context.get('book_id')
        if not book_id:
            raise serializers.ValidationError("Book ID not found in context")
        
        try:
            book = Book.objects.get(id=book_id)
            
            # Check current_borrow_record field
            if book.current_borrow_record:
                raise serializers.ValidationError({
                    'book': 'The book is already borrowed!'
                })
            
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        
        return data


class AdminBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id','book', 'member', 'borrow_date','return_date']
    
    def create(self, validated_data):
        # Get the book from validated_data (admin input)
        book = validated_data.get('book')
        
        if not book:
            raise serializers.ValidationError("Book is required")
        
        # Create the borrow record
        record = BorrowRecord.objects.create(**validated_data)
        
        # Update the book's current borrow record
        book.current_borrow_record = record
        book.save()
        
        return record
    
    def validate_book(self, value):
        if value.current_borrow_record:
            raise serializers.ValidationError("This book is already borrowed and not yet returned")
        return value
    

    def validate(self, data):
        """
        Object-level validation
        """
        return_date = data.get('return_date')
        if return_date:
            today = timezone.now().date()
            max_return_date = today + timedelta(days=30)
            
            if return_date < today:
                raise serializers.ValidationError({
                    'return_date': 'Return date cannot be in the past.'
                })
            
            if return_date > max_return_date:
                raise serializers.ValidationError({
                    'return_date': 'You cannot borrow for more than 30 days.'
                })
        return data