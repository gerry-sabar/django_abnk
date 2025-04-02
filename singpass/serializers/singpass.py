from rest_framework import serializers


class SingpassSerializer(serializers.Serializer):
    auth_state = serializers.CharField(max_length=150, error_messages={
        'required': 'auth_state is required',
        'max_length': 'auth_state must not exceed 150 characters.'
    })

    auth_code = serializers.CharField(max_length=150, error_messages={
        'required': 'auth_code is required',
        'max_length': 'auth_code must not exceed 150 characters.'
    })