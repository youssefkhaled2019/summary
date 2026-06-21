
from . import User
from .. import PostSerializers,request,status,Response,PostوUserSerializer,Post,UserSerializers,UserAdminSerializer,serializers



# ------------------views.py View / APIView--------------------

from django.views import View

class MyView(View):
    def get(self, request):
        pass

"""
----- APIView مبنى على  View -----
Request Object خاص بـ DRF
Response Object خاص بـ DRF
Authentication
Permissions
Throttling
Content Negotiation
Exception Handling


"""
"""
هذه الخصائص ليست من APIView نفسها: 
تستخدم فقط مع GenericAPIView ModelViewSet
queryset
serializer_class
pagination_class
filter_backends
search_fields
ordering_fields
get_object().
get_queryset()

APIView
    ↓
GenericAPIView
    ↓
Mixins
    ↓
Generic Views
    ↓
ViewSets
    ↓
ModelViewSet
"""

class HelloView(APIView):

    def get(self, request):
        return Response({"message": "hello"})
    def post(self, request):
        print(request.data)
        print(request.user)
        print(request.auth) #تعرض بيانات التوكن.

        return Response(request.data)

# ------------------views.py APIView--------------------






# ------------
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

    
# path("rest_cbv/",views.CBV_List.as_view()),
# path("rest_cbv/<int:pK>",views.CBV_pk.as_view()),    

# CBV class based views [ list and create  -> GET POST]
class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] # IsAuthenticated ,IsAdminUser
    throttle_classes = [UserRateThrottle]
    parser_classes = [JSONParser] #تحدد أنواع البيانات المقبولة.
    renderer_classes = [JSONRenderer]
    def get(self, request):
        # posts = Post.objects.filter(user=request.user )
        data=Post.objects.all()
        serializers=PostSerializers(data, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def post(self, request): 
        serializers=PostSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(user=request.user)   #<------ لو   لا تريد  ارسال البيانات مع reqest

        return Response(serializers.data,status=status.HTTP_201_CREATED)
    
    # def post(self,request):
    #     serializer=UserSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #     return Response(  {  "success": False,  "errors": serializer.errors },status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
class PostView_pk(APIView):
    def get_object(self,pK):
        #   try:
        #      return Guest.objects.get(id=pK)
        #   except Guest.DoesNotExist :
        #     raise Http404

        return get_object_or_404(  Guest,  pk=pk)

    def get(self,request,pK):
        # guest = Guest.objects.get(pk=pk)  bset  use  get_object  for  Guest.DoesNotExist
        guest=self.get_object(pK) 
        serializer= UserSerializers(guest)
        return Response(serializer.data)

    def put(self,request,pK):
        guest=self.get_object(pK)
        
        if guest.user != request.user:
           return Response({"error": "Forbidden"}, status=403)
        
        serializer= UserSerializers(guest,data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)#,status=status.HTTP_201_CREATED
        return Response(  {  "success": False,  "errors": serializer.errors },status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(  movie,  data=request.data,  partial=True)#<----
        serializer.is_valid( raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pK):
        guest=self.get_object(pK)
        guest.delete()
        response={"message":"delete data "}
        return Response(response,status=status.HTTP_204_NO_CONTENT)
# ------------ annotate------------
#view
from django.db.models import Count
class UserView(APIView):
    def get(self, request):
        # data=User.objects.all()
        data = User.objects.annotate(post_count=Count("post"))
        if request.user.is_staff:
           serializers=UserAdminSerializer(data, many=True)
        else:
           serializers = UserSerializers(data,many=True)   

        return Response(serializers.data,status=status.HTTP_200_OK)
#serializers

class UserSerializers(serializers.ModelSerializer):
        post_count = serializers.IntegerField(read_only=True)
        class Meta:
           model =User
           fields = [  "id","username","email","post_count"]#"__all__"






#get one 
user = User.objects.first()
serializer = UserSerializer(user) #
serializer.data

#get  many
users = User.objects.all()
serializer = UserSerializer(users,many=True)

#post
serializer = UserSerializer(data=request.data)
if serializer.is_valid():
    print(serializer.validated_data) #serializer.data
    serializer.save() #create() 
else:    
    print(serializer.errors)    


#put / patch
serializer = UserSerializer(instance=user,data=request.data) #partial=True  # ← ده PATCH  ||      partial=False  # default
if serializer.is_valid():
    serializer.save() #update()

# Delete
def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response(status=204)    

# --------
# queryset = self.get_queryset()
# serializer = UserSerializer(queryset, many=True)
# --------
serializer.initial_data  #✔ البيانات الخام من request    | ❌ لسه متعملهاش validation
serializer.validated_data #✔ بيانات تم التحقق منها   |  ✔ جاهزة للحفظ
serializer.data  # ✔ البيانات بعد التحويل لـ JSON | ✔ بتستخدم في response

serializer.errors
# -------- 

# -------- 
#serializers
class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Post.objects.create(**validated_data)
#view
serializer = PostSerializers(  data=request.data,  context={"request": request})
serializer.is_valid(raise_exception=True)
serializer.save()

# -------- 

# --------- لخص 
"""
from django.db.models import Count, Sum
users = User.objects.annotate(post_count=Count("post"),total_likes=Sum("post__likes"),total_comments=Sum("post__comment"))



posts = Post.objects.annotate( user_post_count=Count("user__post"))
users = User.objects.annotate(post_count=Count("post")).order_by("-post_count")

المواضيع المهمة المرتبطة بـ annotate والتي تستحق تعلمها بعد ذلك:
aggregate()
Count
Sum
Avg
Max
Min
F()
Q()
Case و When
Subquery
OuterRef
Prefetch
select_related
values() و values_list()

هذه الأدوات هي التي تُستخدم غالبًا لبناء استعلامات قوية وتحسين الأداء في Django ORM.

"""