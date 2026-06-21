
from django.urls import path,include
from .views import PostView,UserView
urlpatterns = [
    path('',PostView.as_view(),name="post_vies"),
    path('user/',UserView.as_view(),name="post_vies"),
]



# APIView
    # path("rest_cbv/",views.CBV_List.as_view()),
    # path("rest_cbv/<int:pK>",views.CBV_pk.as_view()),