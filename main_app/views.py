from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from main_app.models import Artist
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ArtistForm
import requests

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

# Create your views here.
class About(TemplateView):
    template_name = "about.html"

@method_decorator(login_required, name='dispatch')
class ArtistList(TemplateView):
    template_name = "artist_list.html"

    def get_context_data(self, **kwargs):
        api_url = "https://api.stockdata.org/v1/data/quote?symbols=pypl,AAPL,TSLA,MSFT&api_token=kyo8bsW7uP4xThzSZ6hMFyHRtk5NLYs4ue8gGC6H"
        response = requests.get(api_url)
        var = response.json()
        s = var['data'][0].items()

        context = super().get_context_data(**kwargs)
        print("-----------------")
        context['art'] = s
       
        for k,v in context['art']:
                print(k,"----",v)
        print("-----------------")
        name = self.request.GET.get("name")
        if name != None:
            context["artists"] = Artist.objects.filter(
                name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for {name}"
        else:
            context["artists"] = Artist.objects.filter(user=self.request.user)
            context["header"] = "Trending Artists"
            # print(context)
        return context
    
# class ArtistCreate(CreateView):
#     model = Artist
#     fields = ['name', 'img', 'bio', 'verified_artist','user']
#     template_name = "artist_create.html"
#     success_url = "/"
    
#     # def form_valid(self, form):
#     #     print(form.cleaned_data)


# @method_decorator(login_required, name='dispatch')
# class ArtistDetail(DetailView):
#     model = Artist
#     template_name = "artist_detail.html"
    
#     def __init__(self, **kwargs):
#     # Go through keyword arguments, and either save their values to our
#     # instance, or raise an error.
#        print("------",Artist(self))




######### Functional Based Views

@login_required
def createArtist(request):
    form = ArtistForm()

    if request.method == 'POST':
        print("request- ",request.POST)
        
        form = ArtistForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,"artist_create.html",context) 


@login_required
def SingleArtistDetail(request,pk):
    # var = Artist.objects.get(id=pk)
    # print("------",var)
    var1 = Artist.objects.filter(id=pk)
    print("------",var1[0])
    
    context = {'artist':var1[0]}
    return render(request,"artist_detail.html",context) 


@login_required
def ArtistUpdate(request,pk):
    artist = Artist.objects.get(id=pk)
    form = ArtistForm(instance = artist)
    print("------")
    print(artist.name)
    print(artist.bio)
    print(artist.user.username)
    print(artist.user.first_name)
    print(artist.user.last_name)
    print(artist.user.email)
    print("------")
    
    if request.method == 'POST':
        # print(request.POST)
        form = ArtistForm(request.POST,instance = artist)
        if form.is_valid():
            form.save()
            return redirect('artist_list')
        
    context = {'form':form}
    context['artist'] = artist
    return render(request,"artist_update.html",context) 

# class ArtistUpdate(UpdateView):
#     model = Artist
#     fields = ['name', 'img', 'bio', 'verified_artist']
#     template_name = "artist_update.html"
#     success_url = "/artists/"

@login_required(login_url="login")
def deleteArtist(request, pk):
    artist = Artist.objects.get(id=pk)

    if request.method == 'POST':
        artist.delete()
        return redirect('artist_list')
    
    return render(request,"artist_delete.html",{'artist':artist}) 


class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)

###############
class Stocks(TemplateView):
    template_name = "stock_list.html"

    def get_context_data(self, **kwargs):
        api_url = "https://api.stockdata.org/v1/data/quote?symbols=pypl,AAPL,TSLA,MSFT&api_token=kyo8bsW7uP4xThzSZ6hMFyHRtk5NLYs4ue8gGC6H"
        response = requests.get(api_url)
        var = response.json()
        s = []
        
        #convert array to dictionary array for django
        for i in range(len(var['data'])):
            s.append(var['data'][i].items())
        print(s)
        
        context = super().get_context_data(**kwargs)
        print("-----------------")
        context['stocks'] = s
       
        # for stock in context['stocks']:
        #     # print("-------",stock)
        #     for k,v in stock:
        #         print(k,"----",v)
        print(context)
        
        return context
