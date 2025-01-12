from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewset, CreateBlog , UpdateBlog , ReadBlog , DeleteBlog
from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('users', UserViewset)

urlpatterns = [
    path('blogs/', CreateBlog.as_view({'post': 'create'}) ),
    path('blogs/<int:pk>/', UpdateBlog.as_view({'put': 'update'})),
    path('get-blogs/', ReadBlog.as_view({'get': 'list'}) ),
    path('get-blogs/<int:pk>/', ReadBlog.as_view({'get': 'retrieve'})),
    path('delete-blogs/<int:pk>/', DeleteBlog.as_view({'delete': 'destroy'})),
    path('login/', TokenObtainPairView.as_view())
] + router.urls
