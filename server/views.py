from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User, UserNote
from .serializers import NoteSerializer

import jwt

class RegisterView(APIView):
  def post(self, *args, **kwargs):
    data = self.request.data
    response = {}
    if not data['email']:
      raise ValueError('Email field is required')
    if not data['password']:
      raise ValueError('Password field is required')

    email = data['email']
    password = data['password'] 

    if User.objects.filter(email=email).exists():
      response['error'] = 'User with this email already exists'
      return Response(response)
    else:
      response['success'] = 'User has been created'

    user = User(
      email = email,
      is_active = True
    ) 

    response['email'] = user.email

    user.set_password(password)
    user.save()

    response['id'] = user.id

    return Response(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):
  def post(self, *args, **kwargs):
    data = self.request.data
    email = data['email']
    password = data['password']
    response = {}
    if not email:
      response['error'] = 'Email is required'
      return Response(response)

    if not password:
      response['error'] = 'Passsword is required'
      return Response(response)

    user = User.objects.filter(email=email).first()

    if user is None:
      response['error'] = 'User does not exist'
      return Response(response)

    if not user.check_password(password):
      response['error'] = 'Incorrect Password'
      return Response(response)

    payload = {
      'id':user.id,
      'email':email,
      'password':password
    }
    
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    
    response = {
      'message':'success',
      'jwt': token
    }

    return Response(response)

class TokenValidateView(APIView):
  def post(self, *args, **kwargs):
    token = self.request.data['token']
    response = {}
    try:
      data = jwt.decode(token, 'secret', algorithms=['HS256'])
      if data:
        response = {
          'message':'success',
          'id':data['id'],
          'email':data['email']
        }
    except:
      response = {
        'error':'Not Authenticated'
      }
    return Response(response)


class NoteView(APIView):
  def post(self, *args, **kwargs):
    token = (self.request.data['token'])
    if token:
      data = jwt.decode(token, 'secret', algorithms=['HS256'])
    
      user_id = data['id']
      query_set = UserNote.objects.filter(user = user_id)
    
      serializer = NoteSerializer(query_set, many=True)
      return Response(serializer.data)
    return Response({'message': 'error'})

class NoteCreateView(APIView):
  def post(self, *args, **kwargs):
    serializer = NoteSerializer(data=self.request.data)
    if serializer.is_valid():
      print(serializer.validated_data)
      note = serializer.create(validated_data=serializer.validated_data)
      note_serializer = NoteSerializer(note, many=False)
      return Response(note_serializer.data)
    print(serializer.errors)
    return Response(serializer.data)

class NoteDetailView(APIView):
  def put(self, request, pk):
    note = UserNote.objects.get(id=pk)
    note.title = request.data['title']
    note.note = request.data['note']
    note.save()
    return Response(request.data)

  def delete(self, request, pk):
    note = UserNote.objects.get(id=pk)
    note.delete()
    return Response(request.data)
