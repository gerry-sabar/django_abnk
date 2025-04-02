import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myinfo.client import MyInfoPersonalClientV4
from django.utils.crypto import get_random_string
from django.conf import settings
from requests.exceptions import HTTPError
from .serializers.singpass import SingpassSerializer


class SingpassCallback(APIView):

    def get(self, request):
        return Response({
            "message": "callback received",
            "code": request.GET.get('code')
        }, status=status.HTTP_200_OK)


class SingpassAPI(APIView):

    def get(self, request):
        oauth_state = get_random_string(length=16)
        client = MyInfoPersonalClientV4()
        authorize_url = client.get_authorise_url(oauth_state, settings.CALLBACK_URL)

        return Response({"url": authorize_url, "state": oauth_state}, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            data = json.loads(request.body)        
        except Exception as e:
            return Response({"message": "Request is not JSON"}, status=status.HTTP_400_BAD_REQUEST)            
        
        serializer = SingpassSerializer(data=data)
        if serializer.is_valid() == False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        auth_code = data.get('auth_code')
        auth_state = data.get('auth_state')
        try:
            person_data = MyInfoPersonalClientV4().retrieve_resource(auth_code, auth_state, settings.CALLBACK_URL)
        except HTTPError as e:
            return Response({"message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST) 
        except:
            return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            

        return Response(person_data, status=status.HTTP_200_OK)

