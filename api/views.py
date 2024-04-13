from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSignUpSerializer, UserLoginSerializer, EyePredictSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from api.algorithm.eyepredict import predict
from .models import Disease
from api.algorithm.readData import readData
# Create your views here.

class UserSignUpView(APIView):
    
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            
            return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['username'], password = serializer.validated_data['password'])
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token":token.key, "username" : user.get_username()})
        
        return Response({"error" : "Invalid credentials"},status= status.HTTP_401_UNAUTHORIZED)
    
class EyeDiseasePredictionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    def post(self, request):
        serializer = EyePredictSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            img = serializer.validated_data["image"]
            predictions = predict(img)
            serializer.save(dname=predictions)
            
            data = readData(predictions)
            return Response({"result" : data,"image":serializer.data["image"]})
        return Response(serializer.errors)