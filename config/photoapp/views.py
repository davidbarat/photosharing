import json
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse_lazy
from .models import Photo, User


class PhotoListView(ListView):
    model = Photo     
    template_name = 'photoapp/list.html'
    # queryset= Photo.objects.all()[:6]
    queryset = Photo.objects.filter().order_by('-created')[:8]
    # context_object_name = 'photos'
    context_object_name = 'queryset'

class PhotoAllListView(ListView):
    model = Photo     
    template_name = 'photoapp/list.html'
    paginate_by = 6
    # queryset= Photo.objects.all()[:6]
    queryset = Photo.objects.filter().order_by('-created')
    # context_object_name = 'photos'
    context_object_name = 'queryset'

class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/taglist.html'
    
    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoTagAllView(ListView):
    model = Photo
    # paginate_by = 6
    template_name = 'photoapp/taglistall.html'
    queryset_temp = Photo.objects.all().values_list('tags__slug', flat=True)
    list_tag =  []
    for value in queryset_temp:
         list_tag.append(str(value))

    queryset = set(list_tag)
    context_object_name = 'unique_tag'


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['title', 'description', 'image', 'tags']
    template_name = 'photoapp/create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):
    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))
    
    def test_func(self):
        
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')
            

class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('photo:list')

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')


class PhotoProfileView(LoginRequiredMixin, ListView):
    paginate_by = 6
    model = Photo
    template_name = 'profile.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        user_id = User.objects.filter(
            username=self.request.user).values_list('id', flat=True).last()
        queryset = Photo.objects.filter(submitter_id=user_id)
        return queryset


class PhotoSearchView(ListView):
    # template_name = 'photoapp/search.html'
    paginate_by = 6
    model = Photo
    success_url = reverse_lazy('photo:search')
    
    def get(self, request):
        message = ""
        query = request.GET.get("query")
        if not query:
            message = "Remplissez le champ de recherche"
        else:
            user_id = User.objects.filter(
                username__icontains=query).values_list('id', flat=True).last()
            photo_query_data=serializers.serialize(
                "json",
                Photo.objects.filter(submitter_id=user_id),
                fields=("id", "title", "description", "created", "image"),
            )
            photo_query_data = Photo.objects.filter(submitter_id=user_id)
            # product_query_json = json.loads(photo_query_data)

        context = {
        "query": query,
        "message": message,
        "queryset": photo_query_data,
        }
        return render(request, "photoapp/search.html", context)