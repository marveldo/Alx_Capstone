from django.shortcuts import render
from rest_framework import viewsets , mixins , permissions , response, status, pagination, renderers
from .serializers import UserSerializer , BlogPostSerializer, CustomUser, BlogPost
from django_filters.rest_framework import DjangoFilterBackend

class UserViewset(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [renderers.JSONRenderer]


class CreateBlog(viewsets.GenericViewSet , mixins.CreateModelMixin):

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]


class ReadBlog(viewsets.GenericViewSet , mixins.ListModelMixin , mixins.RetrieveModelMixin):
    
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content', 'tags', 'author', 'published_date']
    renderer_classes = [renderers.JSONRenderer]
    
    

class UpdateBlog(viewsets.GenericViewSet, mixins.UpdateModelMixin):

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
        return response.Response(data , status=status.HTTP_200_OK)

class DeleteBlog(viewsets.GenericViewSet, mixins.DestroyModelMixin):
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


        





