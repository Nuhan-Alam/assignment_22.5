from django.shortcuts import render
from all.serializers import CategorySerializer,AuthorSerializer,BorrowSerializer,BookReadSerializer,BookWriteSerializer,AdminBorrowSerializer
from rest_framework.viewsets import ModelViewSet
from all.models import Category,Author,BorrowRecord,Book
from django.db.models import Count
from all.permission import IsAdminOrReadOnly,IsAdmin
from all.permission import IsReviewAuthorOrReadonly

class CategoryViewSet(ModelViewSet):
    """
    Manage book categories.

    Retrieves, creates, updates, and deletes categories.
    Each category is annotated with the total number of books it contains (`book_count`).
    - **Read-only** for unauthenticated/regular users.
    - **Full access** for admin users.
    """
    queryset = Category.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class AuthorViewSet(ModelViewSet):
    """
    Manage authors.

    Retrieves, creates, updates, and deletes authors.
    Each author is annotated with the total number of books they have written (`book_count`).
    - **Read-only** for unauthenticated/regular users.
    - **Full access** for admin users.
    """
    queryset = Author.objects.annotate(
        book_count=Count('books')).all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    

class BookViewSet(ModelViewSet):
    """
    Manage books.

    Retrieves, creates, updates, and deletes books.
    - Uses `BookWriteSerializer` for create/update operations.
    - Uses `BookReadSerializer` for read operations.
    - Optimized with `select_related` for author and category data.
    - **Read-only** for unauthenticated/regular users.
    - **Full access** for admin users.
    """
    queryset = Book.objects.select_related('author', 'category').all()
    permission_classes = [IsAdminOrReadOnly]
    def get_serializer_class(self):
        """
        Return the appropriate serializer class.

        - Uses `BookWriteSerializer` for create, update, and partial update.
        - Uses `BookReadSerializer` for all other actions.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return BookWriteSerializer
        return BookReadSerializer

class BorrowViewSet(ModelViewSet):
    """
    Manage borrow records for the current user.

    Allows the logged-in user to borrow books and view their own borrow history.
    Automatically injects:
    - `user_id` and `user` into the serializer context.
    - `book_id` from the URL kwargs.
    """
    queryset = BorrowRecord.objects.select_related('book', 'member').all()
    serializer_class = BorrowSerializer

    def get_serializer_context(self):
        """
        Provide extra context to the serializer.

        Context includes:
        - `user_id`: ID of the logged-in user.
        - `user`: the logged-in user object.
        - `book_id`: ID of the book from the URL.
        """
        # if getattr(self, 'swagger_fake_view', False):
        #     return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user,'book_id': self.kwargs['book_pk']}
    
    def get_queryset(self):
        """
        Restrict queryset to the current user's borrow records.
        """
        return BorrowRecord.objects.filter(member_id=self.request.user.id)
    
class AdminBorrowViewSet(ModelViewSet):
    """
    Manage all borrow records (Admin only).

    Retrieves, creates, updates, and deletes borrow records.
    Optimized with `select_related` for book and member data.
    - **Accessible only** to admin users.
    """
    queryset = BorrowRecord.objects.select_related('book', 'member').all()
    serializer_class = AdminBorrowSerializer
    permission_classes = [IsAdmin]