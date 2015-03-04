from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from movies import models, serializers
from django.views.decorators.cache import cache_page
from rest_framework import status


@api_view(['GET'])
def get_movie(request, obj_id):
    try:
        movie = models.Movie.objects.get(id=obj_id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.NestedMovieSerializer(movie, dropfields=('locations',))
    return Response(serializer.data)

@api_view(['GET'])
def get_movies(request):
    movies = models.Movie.objects.all().prefetch_related('locations').select_related('director')
    if movies.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.NestedMovieSerializer(movies, many=True, fields=('id', 'title', 'locations'))
    return Response(serializer.data)

@api_view(['GET'])
def get_locations(request):
    locations = models.Location.objects.all()
    if locations.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.LocationSerializer(locations, many=True)
    return Response(serializer.data)