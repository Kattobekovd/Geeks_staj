from django.shortcuts import render
from rest_framework import status

from . import models
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import TaskSerializer



@api_view(['GET','POST'])
def post_create_api_view(request):
    if request.method == 'GET':
        post = models.Task.objects.all()
        data = TaskSerializer(instance=post, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        completed = request.data.get('completed')
        created = request.data.get('created')

        post = models.Task.objects.create(
            title=title,
            description=description,
            completed=completed,
            created=created
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'post_id': post.id})


@api_view(['GET','PUT','DELETE'])
def post_detail_api_view(request, id):
    try:
        post = models.Task.objects.get(id=id)
    except models.Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': 'POst Not found.'})

    if request.method == 'GET':
        data = TaskSerializer(instance=post, many=True).data
        return Response(data=data)
    elif request.method == 'PUT':
        post.title = request.data.get('title')
        post.description = request.data.get('description')
        post.completed = request.data.get('completed')
        post.created = request.data.get('created')
        post.save()
        return Response(status=status.HTTP_200_OK,
                        data={'post_id': post.id})
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)