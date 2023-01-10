import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from HW27 import settings
from ads.models import Ad, Category, Location, User


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by("-price"), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append(
                {
                    "id": ad.pk,
                    "name": ad.name,
                    "author": ad.author.username,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "image": ad.image.url if ad.image else None,
                    "category": ad.category.name,
                }
            )
        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = [
        'name',
        'author'
        'description',
        'price',
        'is_published',
        'image',
        'category',
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        ad = Ad.objects.create(
            name=data["name"],
            author=data["author"],
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            image=request.FILES["image"],
            category=data["category"],
        )
        return JsonResponse(
            {
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url,
                "category": ad.category.name,
            },
            safe=False
        )


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse(
            {
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url,
                "category": ad.category.name,
            },
            safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = [
        'name',
        'author'
        'description',
        'price',
        'is_published',
        'image',
        'category',
    ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.description = data["description"]
        self.object.price = data["price"]
        self.object.is_published = data["is_published"]
        self.object.image = request.FILES["image"]
        self.object.category = data["category"]
        self.object.save()
        return JsonResponse(
            {
                "id": self.object.pk,
                "name": self.object.name,
                "author": self.object.author.username,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "image": self.object.image.url,
                "category": self.object.category.name,
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(AdDeleteView, self).delete(request, *args, **kwargs)
        return JsonResponse(
            {
                "status": "ok"
            }, status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for category in self.object_list.order_by("name"):
            response.append(
                {
                    "id": category.pk,
                    "name": category.name,
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['id', 'name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category()
        category.name = data["name"]
        category.save()
        return JsonResponse(
            {
                "id": category.pk,
                "name": category.name,
            },
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse(
            {
                "id": category.pk,
                "name": category.name,
            },
            safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["id", "name"]

    def patch(self, request, *args, **kwargs):
        super(CategoryUpdateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()
        return JsonResponse(
            {
                "id": self.object.pk,
                "name": self.object.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse(
            {
                "status": "ok"
            }, status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class LocationListView(ListView):
    model = Location

    def get(self, request, *args, **kwargs):
        super(LocationListView, self).get(request, *args, **kwargs)
        response = []
        for location in self.object_list:
            response.append(
                {
                    "id": location.pk,
                    "name": location.name,
                    "lat": location.lat,
                    "lng": location.lng
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    fields = ["name", "lat", "lng"]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        location = Location
        location.name = data["name"]
        location.lat = data["lat"]
        location.lng = data["lng"]
        location.save()
        return JsonResponse(
            {
                "id": location.pk,
                "name": location.name,
                "lat": location.lat,
                "lng": location.lng,
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        location = self.get_object()
        return JsonResponse(
            {
                "id": location.pk,
                "name": location.name,
                "lat": location.lat,
                "lng": location.lng,
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse(
            {
                "status": "ok"
            }, status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for user in self.object_list.order_by("username"):
            response.append(
                {
                    "id": user.pk,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role,
                    "age": user.age,
                    "location": user.location.name,
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = super().get_object()

        return JsonResponse(
            {
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": user.location.name,
                "total_ads": user.user_ad.count()
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = [
        "id",
        "first_name",
        "last_name",
        "username",
        "password",
        "role",
        "age",
        "location",
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=data["password"],
            role=data["role"],
            age=data["age"],
            location=Location.objects.get_or_create(name=data["location"])
        )
        user.save()
        return JsonResponse(
            {
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": user.location.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        "id",
        "first_name",
        "last_name",
        "username",
        "password",
        "role",
        "age",
        "location",
    ]

    def patch(self, request, *args, **kwargs):
        super(UserUpdateView, self).post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.first_name = data["first_name"],
        self.object.last_name = data["last_name"],
        self.object.username = data["username"],
        self.object.password = data["password"],
        self.object.role = data["role"],
        self.object.age = data["age"],
        self.object.location = Location.objects.get_or_create(name=data["location"])
        self.object.save()
        return JsonResponse(
            {
                "id": self.object.pk,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "password": self.object.password,
                "role": self.object.role,
                "age": self.object.age,
                "location": self.object.location.name,
            }, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super(UserDeleteView, self).delete(request, *args, **kwargs)
        return JsonResponse(
            {
                "status": "ok"
            }, status=200
        )
