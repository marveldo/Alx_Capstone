from django.shortcuts import render
from rest_framework import viewsets , mixins , permissions , response, status, pagination, renderers
from .serializers import UserSerializer , BlogPostSerializer, CustomUser, BlogPost
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewset(viewsets.ModelViewSet):
    """A complete User Viewset To perform all CRUD operations on the User Model

    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [renderers.JSONRenderer]

class LoginView(TokenObtainPairView):
    """The View That Logs In a User

    
    """
    renderer_classes = [renderers.JSONRenderer]


class CreateBlog(viewsets.GenericViewSet , mixins.CreateModelMixin):
    """View to Create A blog User must be Authenticated to create a Blog

    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]


class ReadBlog(viewsets.GenericViewSet , mixins.ListModelMixin , mixins.RetrieveModelMixin):
    """View to Get All blogs and Get one Blog by its ID or primary Key Value

    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content', 'tags', 'author', 'published_date']
    renderer_classes = [renderers.JSONRenderer]
    
    

class UpdateBlog(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """View to Update A blog User Must be Authenticated and be the owner of the blog

    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]

    def update(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.user != request.user :
            error = {
                'message' : 'Not owner of blog'
            }
            return response.Response(status=status.HTTP_401_UNAUTHORIZED, data=error)
        serializer = self.get_serializer(blog , data = request.data , context={'request' : request}, partial=True)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer=serializer)
        return response.Response(serializer.data , status=status.HTTP_200_OK)

class DeleteBlog(viewsets.GenericViewSet, mixins.DestroyModelMixin):
    """View to Delete A blog User Must be Authenticated and must be the owner of the Blog

    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]

    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.user != request.user :
            error = {
                'message' : 'Not owner of blog'
            }
            return response.Response(status=status.HTTP_401_UNAUTHORIZED, data=error)
        blog.delete()
        return response.Response(data={}, status=status.HTTP_204_NO_CONTENT)


        





