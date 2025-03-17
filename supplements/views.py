from django.shortcuts import render
from django.views import View

# Create your views here.
class HomePageView(View):
    template_name = "home.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
class AboutView(View):
    template_name = "about.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
class ProductIndexView(View):
    template_name = "product_index.html"
    
    def get(self, request):
        return render(request, self.template_name)

class ProductView(View):
    template_name = "product.html"
    
    def get(self, request):
        return render(request, self.template_name)

class ProductEditView(View):
    template_name = "products.html"
    
    def get(self, request):
        return render(request, self.template_name)

