
from . import User ,UserSerializer,request,models,Response,Post


# ------------------views.py ModelViewSet--------------------

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (IsAuthenticated,IsAdminUser,AllowAny)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()            
    serializer_class = UserSerializer        
    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def get_queryset(self):
        # return User.objects.all()
        # return User.objects.filter(id=self.request.user.id)
        # return User.objects.annotate(posts_count=Count("posts"))
        # return User.objects.filter(is_active=True)

        # if self.action == "list":return User.objects.all()
        # if self.action == "retrieve":return User.objects.filter(is_active=True)
        # return User.objects.all()
        pass

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny] #        return [AllowAny()]
        elif self.action in ["list","destroy"]:
            permission_classes = [IsAdminUser]
        elif self.action in ["retrieve","update","partial_update"]:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
# ========================
from rest_framework.permissions import BasePermission
class IsOwner(BasePermission):
    def has_object_permission( self, request,view,obj):
        return obj.id == request.user.id    
    
class UserViewSet(ModelViewSet):
    def get_permissions(self):

        if self.action == "create":
            return [AllowAny()]

        return [IsAuthenticated(), IsOwner()]    
# ========================    

