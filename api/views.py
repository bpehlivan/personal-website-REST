from django.db import connection
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json

c = connection.cursor()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })

class Register(APIView):
    def post(self, request, format=None):
        try:
            resp_dict = json.loads(request.body)
            if User.objects.filter(username=resp_dict['username']).exists():
                return Response({'response': "Fail! Username exists!"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(
                username=resp_dict['username'],
                email=resp_dict['email'],
                password=resp_dict['password'],
                first_name=resp_dict['first_name'],
                last_name=resp_dict['last_name']
            )
            user.save()
            return Response({'response': "Success! User created!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response({'error': "Fail! Not registered!"}, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class GetRecords(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        id = request.user.id
        try:
            c.execute("SELECT array_to_json(array_agg(t)) FROM test.record as t WHERE user_id = %s", (id,))
            data = c.fetchall()
            status_code = status.HTTP_200_OK
        except:
            data = 'error occured!'
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response({'response': data[0][0]}, status=status_code)

class SetWeightRecord(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            resp_dict = json.loads(request.body)
            sql = """
            INSERT INTO test.record VALUES(%s, %s, %s, %s)
            ON CONFLICT (user_id, date) DO UPDATE
            SET weight = %s, record_date = %s
            """
            data = (request.user.id, resp_dict['date'], resp_dict['weight'],
                    resp_dict['record time'], resp_dict['weight'], resp_dict['record time'])

            c.execute(sql, data)
            return Response({'response': "Success! your record saved!"},status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'error': "body could not parsed!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            resp_dict = json.loads(request.body)
            sql = """
            DELETE FROM test.record
            WHERE user_id = %s AND date = %s
            """
            data = (request.user.id, resp_dict['date'])
            c.execute(sql, data)
            return Response({'response': "Success, your record deleted!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'error': "body could not parsed!"}, status=status.HTTP_400_BAD_REQUEST)
