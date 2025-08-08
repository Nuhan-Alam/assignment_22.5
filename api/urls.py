from django.urls import path, include
from all.views import CategoryViewSet,AuthorViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet,basename='category')
router.register('authors', AuthorViewSet,basename='author')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('', include(product_router.urls)),
    # path('', include(cart_router.urls))
]