import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category, Location, User


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []

        for ad in self.object_list:
            response.append(
                {
                    "id": ad.pk,
                    "name": ad.name,
                    "author": ad.author.name,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "image": ad.image,
                    "category": ad.category.name,
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = [
        'name',
        'author_id'
        'description',
        'price',
        'is_published',
        'image',
        'category_id',
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        ad = Ad.objects.create(
            name=data["name"],
            author_id=data["author_id"],
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            image=data["image"],
            category_id=data["category_id"],
        )
        return JsonResponse(
            {
                "id": ad.pk,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image,
                "category_id": ad.category_id,
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
                "author": ad.author.name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image,
                "category": ad.category.name,
            },
            safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for category in self.object_list:
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
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for user in self.object_list:
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
        user = User
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.username = data["username"]
        user.password = data["password"]
        user.role = data["role"]
        user.age = data["age"]
        user.location = data["location"]
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
