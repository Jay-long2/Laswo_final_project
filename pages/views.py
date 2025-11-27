from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'title': 'Home - Laswo Studios',
    }
    return render(request, 'pages/home.html', context)

def about(request):
    context = {
        'title': 'About Us - Laswo Studios',
    }
    return render(request, 'pages/about.html', context)

def contact(request):
    context = {
        'title': 'Contact - Laswo Studios',
    }
    return render(request, 'pages/contact.html', context)