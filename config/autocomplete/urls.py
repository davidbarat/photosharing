from django.urls import path

from .views import AutocompleteView

app_name = 'autocomplete'

urlpatterns = [path('', AutocompleteView.as_view(), name='complete')]