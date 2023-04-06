from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from hearts.models import Heart
from hearts.serializers import HeartSerializers
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def heart_list(request):
    # GET list of hearts, POST a new heart, DELETE all hearts

    # retrieve objects (with condition)
    # retrieve all Hearts / find by term from PostgreSQL database
    if request.method == 'GET':
        hearts = Heart.objects.all()

        term = request.GET.get('term', None)
        if term is not None:
            # partial value (similar to same)
            hearts = hearts.filter(term__icontains=term)

        hearts_serializers = HeartSerializers(hearts, many=True)
        return JsonResponse(hearts_serializers.data, safe=False)
        # 'safe=False' for objects serialization

    # create a new object
    # create and save a new Heart
    elif request.method == 'POST':
        heart_data = JSONParser().parse(request)
        heart_serializer = HeartSerializers(data=heart_data)
        if (heart_serializer.is_valid()):
            heart_serializer.save()
            return JsonResponse(heart_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(heart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete all objects
    # delete all Hearts from database
    elif request.method == 'DELETE':
        count = Heart.objects.all().delete()
        print(f"count = {count}")   # DEBUG
        return JsonResponse({'message': '{} Hearts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def heart_detail(request, pk):
    #  GET / PUT / DELETE heart
    # ... heart = Heart.objects.get(pk=pk)
    # ...
    # find heart by pk (id)
    try:
        heart = Heart.objects.get(pk=pk)
    except Heart.DoesNotExist:
        return JsonResponse({'message': 'The heart does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # retrieve a single object
    # find a single Heart with an id
    if request.method == 'GET':
        heart_serializer = HeartSerializers(heart)
        return JsonResponse(heart_serializer.data)

    # update an object
    # update a Heart by the id in the request
    elif request.method == 'PUT':
        print(f"HERE: request = {request}")
        heart_data = JSONParser().parse(request)
        print(f"HERE: heart_data = {heart_data}")
        heart_serializer = HeartSerializers(heart, data=heart_data)
        if heart_serializer.is_valid():
            heart_serializer.save()
            return JsonResponse(heart_serializer.data)
        return JsonResponse(heart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an object
    # delete a Heart with the specified id
    elif request.method == 'DELETE':
        heart.delete()
        return JsonResponse({'message': 'Heart was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# v1 api for getHeartByTerm


@api_view(['GET', 'POST'])
def heart_list_v1(request, total=None):
    pk = 1   # assume only one data
    # find heart by pk (id)
    try:
        heart = Heart.objects.get(pk=pk)
    except Heart.DoesNotExist:
        return JsonResponse({'message': 'The heart does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # retrieve a single object
    # find a single Heart with an id
    if request.method == 'GET':
        heart_serializer = HeartSerializers(heart)
        return JsonResponse(heart_serializer.data)

    elif request.method == 'POST':
        """print("=== HERE ===")
        print(f"request = {request}")
        print(f"total = {total}")"""

        if total is not None:
            # TODO: heart_data = {"total": total}
            heart_data = dict()
            currTotal = getattr(heart, "total")
            heart_data["total"] = currTotal + int(total)
            # print(f"heart_data = {heart_data}")

            # serialize & save into db
            heart_serializer = HeartSerializers(
                heart, data=heart_data)   # type: ignore
            # print(f"heart_serializer = {heart_serializer}")

            if (heart_serializer.is_valid()):
                heart_serializer.save()
                return JsonResponse({'message': 'Heart total is updated successfully!'}, status=status.HTTP_204_NO_CONTENT)
            return JsonResponse(heart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'total field is required!'}, status=status.HTTP_400_BAD_REQUEST)
