
from . import User ,UserSerializer,request,models,Response,Post


# ------------------models.py--------------------

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField()
# ------------------Serializer.py--------------------
from django.core.validators import MinLengthValidator
from rest_framework import serializers

class User_2_Serializer(serializers.Serializer):  # logic عايز تعمل  خاص | Model  عايز تجمع بيانات من أكتر من  |  
    mobile = serializers.RegexField(regex=r'^01[0-9]{9}$', error_messages={"invalid": "Invalid mobile number (must start with 01 and be 11 digits)" })
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField() #✔ بيعمل validation تلقائي للإيميل
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(source="is_staff", read_only=True) #source="is_staff", model = User  هنا لو بتسنخدم مودل   غير 
    created_at = serializers.DateTimeField()
    price = serializers.FloatField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) #[✔ يرجع ID] [✔ ويستخدم في create/update]
    user = serializers.SlugRelatedField(slug_field="username",queryset=User.objects.all()) #[✔ بدل ID يستخدم username]
    user = UserSerializer()
    id = serializers.ReadOnlyField() #[✔ عرض فقط]

    # 3) Relation Fields (ForeignKey / ManyToMany)
    # Nested Serializer
    # -----------------
    """ example use  serializers.Serializer with  view
    # serializers
    class DashboardSerializer(serializers.Serializer):
        users_count = serializers.IntegerField()
        posts_count = serializers.IntegerField()
    # view
    data = {"users_count": User.objects.count(), "posts_count": Post.objects.count()}
    serializer = DashboardSerializer(data)
    """
    # -----------------

    #  [✔ مش مربوط بأي Model,
    # ✔ أنت اللي بتكتب create/update بنفسك,
    # ✔ دمج بيانات من أكتر من table
    # ✔ Dashboard stats / reports  ,  ✔ Aggregation results ]
    def create(self, validated_data):
       return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
    
    def get_full_name(self, obj):
        return obj.username.upper()
    


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class User_2_Serializer(serializers.ModelSerializer):
    mobile = serializers.RegexField(regex=r'^01[0-9]{9}$', error_messages={"invalid": "Invalid mobile number (must start with 01 and be 11 digits)" })
    username = serializers.CharField(validators=[ MinLengthValidator(4)])
    full_name = serializers.SerializerMethodField() #method
    password = serializers.CharField(write_only=True) #password add in  fields but only write 
    profile = ProfileSerializer(read_only=True) #fields = ["id", "title", "profile"]  nesed data عشان اظهر  |  [❌ ده يعمل مشكلة في create/update] [لأن Django مش بيعرف يحفظ object nested مباشرة]
    user = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = User
        # fields = "__all__" #["password"] #pk ,reservation use forn_key show in model
        # exclude = ["password"]  # not work with  fields     # exclude or  fields with  model  ❌ مينفعش تستخدم fields + exclude مع بعض
        # read_only_fields = ["id"]                          #تظهر في response
        # extra_kwargs = {"password": {"write_only": True},
                        # "email": {"required": True},  'reservation': {'read_only': True}
                        #     "username": {"min_length": 3} }  #password → يتبعت في request لكن لا يظهر في response
        # depth = 1  # defoult =0   #{"user": 1} ==0 ->  "user": {"id": 1, "username": "ali"} ==1

    def create(self, validated_data):
        # return User.objects.create(**validated_data)

        # password = validated_data.pop("password")
        # user = User.objects.create(**validated_data)
        # user.set_password(password)
        # user.save()
        # return user



        username = validated_data.pop("username")
        email = validated_data.pop("email")
        user = User.objects.create(username=username,email=email)
        profile = Profile.objects.create(user=user,**validated_data)
        return profile

    def update(self, instance, validated_data):

        # instance.username = validated_data.get("username",instance.username)
        # instance.email = validated_data.get("email",instance.email)
        # instance.save()
        # return instance  

        
        # user_data = validated_data.pop("user", None)
        # if user_data:
        #     user = instance.user
        #     user.username = user_data.get("username", user.username)
        #     user.save()
        # instance.phone = validated_data.get("phone", instance.phone)
        # instance.save()
        # return instance  

        # from django.db.models import F
        # User.objects.filter(id=1).update(login_count=F("login_count") + 1)

        # with transaction.atomic():
        #      user = User.objects.select_for_update().get(id=1)

        # user_data = validated_data.pop("user", None)
        # if user_data:
        #     User.objects.filter(id=instance.user_id).update( **user_data)
        # Profile.objects.filter(id=instance.id).update( **validated_data)
        # instance.refresh_from_db() #عشان يرجع أحدث data بعد الـ update
        # return instance
        pass
    
    def validate_username(self, value):
        #  password = self.initial_data.get("password")
        #  if password == value:pass

        if len(value) < 4:
            raise serializers.ValidationError("username too short")
        return value
    
    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")
        if username == password:pass


        if attrs["username"] == attrs["email"]:
            raise serializers.ValidationError(    "username and email can't be same")
        return attrs
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
        # return obj.products.count() annotate  لكن هذا قد يسبب مشكلة N+1 Query إذا كان لديك عدد كبير من السجلات.
        #    return obj.review_set.count()
    def to_representation(self, instance):     #{"id": 1, "username": "youssef", "welcome": "hello"}
        # data = super().to_representation(instance)
        # data["welcome"] = "hello"
        # return data
    
        data = super().to_representation(instance)
        request = self.context["request"]
        if request.user != instance:
            data.pop("email")
        return data

# ------------------
# models
class User(models.Model):
    username = models.CharField(max_length=100)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
# serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # user = UserSerializer() oto ||  user = UserSerializer() ForeignKey  || users = UserSerializer(many=True) ManyToMany
    class Meta:
        model = Profile
        fields = ["id", "user", "phone"]
# {
#     "id": 1,
#     "user": {
#         "id": 3,
#         "username": "ali"
#     },
#     "phone": "010000"
# }
# ------------------
# serializers
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)   
    user_id = serializers.PrimaryKeyRelatedField( queryset=User.objects.all(),  source="user",  write_only=True )
    class Meta:
        model = Post
        fields = ["id", "title", "user", "user_id"]
# GET
{
    "id": 1,
    "title": "post",
    "user": {
        "id": 3,
        "username": "ali"
    }
}
# POST
{
    "title": "post",
    "user_id": 3     # nested model  ياعنى انت تقدر تغير مين كتب البوست دا  تغير مالك عشان فى مشكله فى 
}
# ------------------

# عند الإنشاء (POST) عاوز بعض الحقول تكون اختيارية، ومش لازم أبعتها كلها.

# 1
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False) #<-----
    phone = serializers.CharField(  required=False, allow_null=True)  #<----- #   allow_null=True  لو مسموح تكون القيمة null:
                                                                        # {   "username": "ali", "phone": null}
# 2
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = { "email": {"required": False}, "phone": {"required": False}, } #<-----

    def create(self, validated_data):
        phone = validated_data.get("phone")   #<-----  use validated_data.get("phone") if not found not do any thing
        return User.objects.create(username=validated_data["username"], phone=phone) #validated_data["username"] error if not found username

# 3
phone = models.CharField(max_length=20,blank=True,null=True)  #لو الحقل في الموديل: غالبًا DRF هيعتبره اختياري تلقائيًا. 

# ------------------
# fields هل ممكن احدد اسماء الموجوده بداخل على حسب الركويست

# 1
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and not request.user.is_staff:
            self.fields.pop("is_staff", None)

# 2 GET /users/?fields=id,username   [Query Parameter]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            fields = request.query_params.get("fields")
            if fields:
                allowed = set(fields.split(","))
                existing = set(self.fields)
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

# 3
"""
#note request = self.context.get("request")  لكي يعمل:
لازم تمرر الـ request للـ serializer.

في ViewSet و GenericAPIView بيتم تمريره تلقائيًا:
serializer = UserSerializer( queryset, many=True, context={"request": request})
وفي ModelViewSet و ListAPIView و RetrieveAPIView DRF بيعمل ده تلقائيًا.
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request") 
        if request and request.method == "GET":
            fields.pop("email", None)
            # fields.pop("date_joined")

        return fields

# view
serializer = UserSerializer( queryset, many=True, context={"request": request})
# ------------------
# serializers
class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]
class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"        
# view APIView -> get
def get(self, request):

    if request.user.is_staff:
        serializer = UserAdminSerializer(request.user)
    else:
        serializer = UserPublicSerializer(request.user)

    return Response(serializer.data)        