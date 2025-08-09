from django.shortcuts import render
from all.serializers import CategorySerializer,AuthorSerializer,BorrowSerializer,BookReadSerializer,BookWriteSerializer,AdminBorrowSerializer
from rest_framework.viewsets import ModelViewSet
from all.models import Category,Author,BorrowRecord,Book
from django.db.models import Count
from all.permission import IsAdminOrReadOnly,IsAdmin
from all.permission import IsReviewAuthorOrReadonly

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author', 'category').all()
    permission_classes = [IsAdminOrReadOnly]
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookWriteSerializer
        return BookReadSerializer

class BorrowViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.select_related('book', 'member').all()
    serializer_class = BorrowSerializer

    def get_serializer_context(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user,'book_id': self.kwargs['book_pk']}
    
    def get_queryset(self):
        return BorrowRecord.objects.filter(member_id=self.request.user.id)
    
class AdminBorrowViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.select_related('book', 'member').all()
    serializer_class = AdminBorrowSerializer
    permission_classes = [IsAdmin]