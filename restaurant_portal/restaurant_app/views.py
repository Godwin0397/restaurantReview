from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from restaurant_app.models import Employees, Restaurant, RestaurantReview
from restaurant_app.serializer import EmployeesModelSerializer, RestaurantModelSerializer, RestaurantReviewModelSerializer, combinedModelSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def get_employees(request):
    if request.method=='GET':
        qs = Employees.objects.all()
        respObj = EmployeesModelSerializer(qs, many=True).data
        return Response(respObj, status=status.HTTP_200_OK)

    if request.method=='POST':
        data = request.data
        if type(data) is dict:
            responseSerializer = EmployeesModelSerializer(data=data)
        else:
            responseSerializer = EmployeesModelSerializer(data=data, many=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def update_employees(request, pk):

    def get_object(pk):
        try:
            return Employees.objects.get(id=pk)
        except Employees.DoesNotExist:
            return None

    if request.method=='PUT':
        qs = get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        responseSerializer = EmployeesModelSerializer(qs, data=request.data, partial=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        qs = get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        qs.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class getEmployeesAPIViewSet(APIView, PageNumberPagination):
    def get(self, request):
        qs = Employees.objects.all()
        # responseSerializer = EmployeesModelSerializer(qs, many=True).data
        # return Response(responseSerializer, status=status.HTTP_200_OK)

        # below code is for pagination
        paginatedQs = self.paginate_queryset(qs, request, view=self)
        responseSerializer = EmployeesModelSerializer(paginatedQs, many=True).data
        return self.get_paginated_response(responseSerializer)


    def post(self, request):
        data = request.data
        if type(data) is dict:
            responseSerializer = EmployeesModelSerializer(data=data)
        else:
            responseSerializer = EmployeesModelSerializer(data=data, many=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateEmployeesAPIViewSet(APIView):

    def get_object(self,pk):
        try:
            return Employees.objects.get(id=pk)
        except Employees.DoesNotExist:
            return None
    
    def put(self, request, pk):    
        qs = self.get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        responseSerializer = EmployeesModelSerializer(qs, data=request.data, partial=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        qs = self.get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        qs.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class getEmployeesViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Employees.objects.all()

    def get_object(self, pk):
        try:
            return Employees.objects.get(id=pk)
        except Employees.DoesNotExist:
            return None

    
    def list(self, request):
        qs = self.get_queryset()
        responseSerializer = EmployeesModelSerializer(qs, many=True).data
        return Response(responseSerializer, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        if type(data) is dict:
            responseSerializer = EmployeesModelSerializer(data=data)
        else:
            responseSerializer = EmployeesModelSerializer(data=data, many=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        qs = self.get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        responseSerializer = EmployeesModelSerializer(qs).data
        return Response(responseSerializer, status=status.HTTP_200_OK)

    def update(self, request, pk):
        qs = self.get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        responseSerializer = EmployeesModelSerializer(qs, data=request.data, partial=True)
        if responseSerializer.is_valid()==True:
            responseSerializer.save()
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(responseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        qs = self.get_object(pk)
        if qs==None:
            return Response({"message": "Object does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        qs.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class updateEmployeesModelViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = EmployeesModelSerializer


class combinedModelViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    serializer_class = combinedModelSerializer

    def create(self, request):
        data = request.data
        restaurantdata = data.pop("restaurant")[0]
        restaurantreviewdata = restaurantdata.pop("restaurantReview")[0]

        empData = EmployeesModelSerializer(data=data)
        if empData.is_valid()==True:
            empData.save()
            # return Response(empData.data, status=status.HTTP_201_CREATED)
        else:
            return Response(empData.errors, status=status.HTTP_400_BAD_REQUEST)
        
        restData = RestaurantModelSerializer(data=restaurantdata)
        if restData.is_valid()==True:
            restData.save()
            # return Response(restData.data, status=status.HTTP_201_CREATED)
        else:
            return Response(restData.errors, status=status.HTTP_400_BAD_REQUEST)
        
        restreviewData = RestaurantReviewModelSerializer(data=restaurantreviewdata)
        if restreviewData.is_valid()==True:
            restreviewData.save()
            # return Response(restreviewData.data, status=status.HTTP_201_CREATED)
        else:
            return Response(restreviewData.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'employee': empData.data, 'restaurant': restData.data, 'restaurantreview': restreviewData.data}, status=status.HTTP_201_CREATED)