from django.urls import path, include
from all.views import CategoryViewSet,AuthorViewSet,BorrowViewSet,BookViewSet,AdminBorrowViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet,basename='category')
router.register('authors', AuthorViewSet,basename='author')
router.register('borrow', AdminBorrowViewSet,basename='borrow')
router.register('books', BookViewSet,basename='book')

borrow_router = routers.NestedSimpleRouter(router, 'books', lookup='book')

borrow_router.register('borrow', BorrowViewSet, basename='book-borrow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(borrow_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('rest_framework.urls'))
    # path('', include(product_router.urls)),
    # path('', include(cart_router.urls))
]