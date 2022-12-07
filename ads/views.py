import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad, Category


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()
        response = []
        for ad in ads:
            response.append(
                {
                    "id": ad.pk,
                    "name": ad.name,
                    "author": ad.author,
                    "price": ad.price,
                    "description": ad.description,
                    "address": ad.address,
                    "is_published": ad.is_published,
                }
            )
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        ad = Ad()
        ad.name = data["name"]
        ad.author = data["author"]
        ad.price = data["price"]
        ad.description = data["description"]
        ad.address = data["address"]
        ad.is_published = data["is_published"]
        ad.save()
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
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
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
