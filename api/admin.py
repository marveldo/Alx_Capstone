from django.contrib import admin
from .models import CustomUser , BlogPost , Tag
# Register your models here.

models_list = [CustomUser , BlogPost , Tag]

for model in models_list :
    admin.site.register(model)