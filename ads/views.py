import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView

from ads.models import Ad, Category


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ads = self.object_list
        response = []
        for ad in ads:
            response.append(
                {
                    "id": ad.pk,
                    "name": ad.name,
                    "price": ad.price,
                    "description": ad.description,
                    "is_published": ad.is_published,
                    "test": ad.image
                }
            )
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = [
        'name',
        'description',
        'price',
        'is_published',
        'image',
    ]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        ad = Ad.objects.create(
            name=data["name"],
            author=data["author"],
            price=data["price"],
            description=data["description"],
            address=data["address"],
            is_published=data["is_published"],
        )
        return JsonResponse(
            {
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
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
                # "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                # "address": ad.address,
                "is_published": ad.is_published,
            },
            safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []
        for category in categories:
            response.append(
                {
                    "id": category.pk,
                    "name": category.name,
                }
            )
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        category = Category()
        category.name = data["name"]
        category.save()
        return JsonResponse(
            {
                "id": category.pk,
                "name": category.name,
            },
            safe=False
        )


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
