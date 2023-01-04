from django.contrib import admin

from ads.models import User, Category, Ad, Location

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Location)
# Register your models here.
