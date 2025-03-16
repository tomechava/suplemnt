from django.shortcuts import render
from django.views import View

# Create your views here.
class HomePageView(View):
    template_name = "supplements/home.html"
    
    def get(self, request):
        return render(request, self.template_name)