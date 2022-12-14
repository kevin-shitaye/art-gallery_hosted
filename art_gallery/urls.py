from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'art_gallery'

router= DefaultRouter()

router.register('art', ArtView, basename='art')
router.register('client', ClientView, basename='client')
router.register('category', CategoryView, basename='category')
router.register('transaction', TransactionView, basename='transaction')
router.register('text_content', TextContent, basename='text_content')
router.register('image_content', ImageContent, basename='image_content')
router.register('email', Email, basename='email')
router.register('subscribe', Subscribe, basename='subscribe')
router.register('unsubscribe', UnSubscribe, basename='unsubscribe')
router.register('contactme', ContactMe, basename="contactme")

urlpatterns = [
    path('', include(router.urls)),
    path('account/<int:pk>', AccountView().as_view(), name='user'),
]
