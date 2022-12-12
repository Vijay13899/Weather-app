from django.shortcuts import render
import requests
from .forms import CityForm
from .models import City
# Create your views here.

def index(request):
    cities = City.objects.all()
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=236ae9460b4d6f55f1e45881464d85d6"
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            if City.objects.filter(name=n).exists():
                pass
            else:
                form.save()
    weather_data = []
    for city in cities:
        response = requests.get(url.format(city))
        if response.status_code == 404:
            continue
        city_weather = response.json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'country': city_weather['sys']['country'],
            'sunrise': city_weather['sys']['sunrise'],
            'sunset': city_weather['sys']['sunset'],
            'windspeed': city_weather['wind']['speed']
        }
        weather_data.append(weather)
    context = {
        'weather_data':weather_data,
        'form':form,
    }
    return render(request,'index.html',context)