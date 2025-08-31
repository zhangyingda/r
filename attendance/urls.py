from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'groups',views.GroupViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('graphql',csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('students/', views.search_students)
]+debug_toolbar_urls()