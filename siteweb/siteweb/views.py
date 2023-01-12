from django.shortcuts import render

def homepage_render(request):
    page = render(request, "homepage.html")
    return page