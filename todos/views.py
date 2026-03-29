from django.shortcuts import render
from todos.serializers import TodosSerializer
from rest_framework.decorators import APIView
from todos.models import Todos
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.


class TodosApiView(APIView):

    # get all data
    def get(self,request):
        # filter by user
        todos = Todos.objects.filter(user = request.user)
        # check useing serialzer
        serializer = TodosSerializer(todos,many=True)
       
        return Response(serializer.data)
    
    # post todos
    def post(self,request):
        serializer = TodosSerializer(data = request.data)
        # print(serializer.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.user)
        return Response(serializer.data)


class TodosDetilsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk, user):
        return get_object_or_404(Todos,pk=pk,user = user)
    

    def get(self,request,pk):
        todo = self.get_object(pk,request.user)
        serializer = TodosSerializer(todo)
        return Response(serializer.data)
    
    def put(self, request, pk):
        todo = self.get_object(pk,request.user)
        serializer = TodosSerializer(todo, data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.user)
        
        return Response(serializer.data)
    
    def patch(self, request,pk):
        todo = self.get_object(pk,request.user)
        serializer = TodosSerializer(todo,data = request.data, partial = True)

        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.user)

        return Response()
    
    def delete(self,request,pk):
        todo = self.get_object(pk, request.user)
        todo.delete()
        return Response({"message":'Delete success'})
    
    def post(self,request,pk):
        todo = self.get_object(pk,request.user)
        todo.is_completed = True
        todo.is_archived = True
        todo.save()

        return Response({"message":"This Task is completed"})

    