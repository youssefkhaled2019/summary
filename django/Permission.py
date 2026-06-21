from rest_framework.permissions import BasePermission
from rest_framework import permissions
class IsOwner(BasePermission):
    def has_object_permission(self,request, view, obj ):
        return obj.user == request.user
    






class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  #SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return obj.author == request.user  #delete,update
    


class IsAuthor(BasePermission):    
    def has_object_permission(self, request, view, obj):
        print(request.user)
        return obj.author == request.user# username and password

    # def has_object_permission(self, request, view, obj):
    #     return super().has_object_permission(request, view, obj)
    
    # def has_permission(self, request, view):
    #     return super().has_permission(request, view)



