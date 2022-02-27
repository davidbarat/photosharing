'''Photoapp URL patterns'''

from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    PhotoListView,
    PhotoTagListView,
    PhotoTagAllView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    PhotoProfileView,
    PhotoSearchView,
    PhotoAllListView
)

app_name = 'photo'

urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),
    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),
    path('photo/tag/', PhotoTagAllView.as_view(), name='alltag'),
    path('photo/all/', PhotoAllListView.as_view(), name='allphoto'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),
    path('photo/create/', login_required(PhotoCreateView.as_view()), name='create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),
    path('photo/profile/', login_required(PhotoProfileView.as_view()), name='profile'),
    path('photo/search/', PhotoSearchView.as_view(), name='search'),
]
