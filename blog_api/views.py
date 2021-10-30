from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions, IsAuthenticatedOrReadOnly

'''
Permissions
View - GET
Delete - DELETE
Change - PUT PATCH
Add - POST
'''


class PostUserWritePermission(BasePermission):
    """
    Custom permission to ensure only the author of a Post object
    can access non SAFE_METHODS to the endpoint
    """
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        # to check if the request method is among the safe methods
        # else only permit (return True) if the author is the user
        # making the request
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


"""
CreateAPIView
Used for create-only endpoints.
Provides a post method handler.

ListAPIView
Used for read-only endpoints to represent a collection of model instances.
Provides a get method handler.

RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
Provides a get method handler.

DestroyAPIView
Used for delete-only endpoints for a single model instance.
Provides a delete method handler.

UpdateAPIView
Used for update-only endpoints for a single model instance.
Provides put and patch method handlers.

ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
Provides get and post method handlers.

RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
Provides get, put and patch method handlers.

RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
Provides get and delete method handlers.

RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
Provides get, put, patch and delete method handlers.
"""
